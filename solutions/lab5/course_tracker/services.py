from __future__ import annotations
import copy
import csv
import functools
import logging
import sys
import tracemalloc
from collections.abc import Callable, Generator, Iterable, Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from course_tracker.exceptions import (
    CourseTrackerError,
    DuplicateError,
    NotFoundError,
    StorageError,
    ValidationError,
)
from course_tracker.models import Lab, Student, Submission
from course_tracker.storage import JsonStateStorage, export_to_csv, export_to_json


def setup_logger() -> logging.Logger:
    Path("data").mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("course_tracker")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("data/course_tracker.log", encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


logger = setup_logger()


def logged_mutation(func: Callable) -> Callable:
    """Декоратор: логирует вызов и оборачивает изменение состояния в транзакцию."""
    @functools.wraps(func)
    def wrapper(self: Course, *args, **kwargs):
        logger.info("Вызов %s args=%s kwargs=%s", func.__name__, args, kwargs)
        try:
            with self.transaction():
                result = func(self, *args, **kwargs)
            logger.info("Успешно: %s", func.__name__)
            return result
        except CourseTrackerError as e:
            logger.warning("Ошибка предметной области в %s: %s", func.__name__, e)
            raise
        except Exception as e:
            logger.error("Непредвиденная ошибка в %s: %s", func.__name__, e)
            raise
    return wrapper


class Course:
    def __init__(self, storage: JsonStateStorage | None = None):
        self.students: dict[str, Student] = {}
        self.labs: dict[str, Lab] = {}
        self.submissions: list[Submission] = []
        self.storage = storage or JsonStateStorage()
        self._manual_snapshot: dict | None = None
        self._undo_stack: list[dict] = []

    # --- Специальные методы (итерационная модель) ---
    def __iter__(self) -> Iterator[Student]:
        return iter(self.students.values())

    def __len__(self) -> int:
        return len(self.students)

    def __contains__(self, item_id: str) -> bool:
        return item_id in self.students or item_id in self.labs

    # --- Снимки, транзакции и откат ---
    def _capture_state(self) -> dict:
        return copy.deepcopy(
            {
                "students": self.students,
                "labs": self.labs,
                "submissions": self.submissions,
            }
        )

    def _apply_state(self, state: dict) -> None:
        self.students = copy.deepcopy(state["students"])
        self.labs = copy.deepcopy(state["labs"])
        self.submissions = copy.deepcopy(state["submissions"])

    @contextmanager
    def transaction(self):
        before = self._capture_state()
        try:
            yield
            self._undo_stack.append(before)
        except Exception:
            self._apply_state(before)
            raise

    def create_snapshot(self) -> None:
        self._manual_snapshot = self._capture_state()

    def restore_snapshot(self) -> None:
        if self._manual_snapshot is None:
            raise ValidationError("Снимок состояния еще не создан.")
        self._undo_stack.append(self._capture_state())
        self._apply_state(self._manual_snapshot)

    def undo(self) -> None:
        if not self._undo_stack:
            raise ValidationError("Нет действий для отмены.")
        previous_state = self._undo_stack.pop()
        self._apply_state(previous_state)

    # --- Сохранение и загрузка ---
    def save_state(self) -> None:
        payload = {
            "students": [s.to_dict() for s in self.students.values()],
            "labs": [lab.to_dict() for lab in self.labs.values()],
            "submissions": [sub.to_dict() for sub in self.submissions],
        }
        self.storage.save_atomic(payload)

    def load_state(self) -> None:
        data = self.storage.load()
        if not data:
            return
        self.students = {
            item["student_id"]: Student.from_dict(item) for item in data.get("students", [])
        }
        self.labs = {
            item["lab_id"]: Lab.from_dict(item) for item in data.get("labs", [])
        }
        self.submissions = [
            Submission.from_dict(item) for item in data.get("submissions", [])
        ]

    # --- Управление студентами ---
    @logged_mutation
    def register_student(self, student_id: str, full_name: str, group: str) -> Student:
        if student_id in self.students:
            raise DuplicateError(f"Студент с ID '{student_id}' уже зарегистрирован.")
        student = Student(student_id=student_id, full_name=full_name, group=group)
        self.students[student_id] = student
        return student

    def get_student(self, student_id: str) -> Student:
        student = self.students.get(student_id)
        if not student:
            raise NotFoundError(f"Студент '{student_id}' не найден.")
        return student

    def list_students(self, sort_by: str = "id") -> list[Student]:
        key_map = {
            "id": lambda s: s.student_id,
            "name": lambda s: s.full_name.lower(),
            "group": lambda s: s.group.lower(),
        }
        if sort_by not in key_map:
            raise ValidationError("Сортировка возможна только по: id, name, group.")
        return sorted(self.students.values(), key=key_map[sort_by])

    @logged_mutation
    def set_student_active(self, student_id: str, active: bool) -> Student:
        student = self.get_student(student_id)
        student.active = active
        return student

    def search_students(self, query: str) -> list[Student]:
        q = query.strip().lower()
        return [
            s
            for s in self.students.values()
            if q in s.student_id.lower() or q in s.full_name.lower() or q in s.group.lower()
        ]

    # --- Управление лабораторными работами ---
    @logged_mutation
    def create_lab(
        self,
        lab_id: str,
        title: str,
        max_score: float,
        deadline: datetime,
        tags: Iterable[str] | None = None,
        description: str = "",
    ) -> Lab:
        if lab_id in self.labs:
            raise DuplicateError(f"Лабораторная работа '{lab_id}' уже существует.")
        lab = Lab(
            lab_id=lab_id,
            title=title,
            description=description,
            max_score=max_score,
            deadline=deadline,
            tags=tags,
        )
        self.labs[lab_id] = lab
        return lab

    def get_lab(self, lab_id: str) -> Lab:
        lab = self.labs.get(lab_id)
        if not lab:
            raise NotFoundError(f"Лабораторная работа '{lab_id}' не найдена.")
        return lab

    def list_labs(self) -> list[Lab]:
        return sorted(self.labs.values(), key=lambda l: l.lab_id)

    def search_labs(self, query: str) -> list[Lab]:
        q = query.strip().lower()
        return [
            lab
            for lab in self.labs.values()
            if q in lab.title.lower()
            or q in lab.description.lower()
            or any(q in tag for tag in lab.tags)
        ]

    # --- Попытки сдачи ---
    @logged_mutation
    def submit_lab(
        self,
        student_id: str,
        lab_id: str,
        score: float,
        comment: str = "",
    ) -> Submission:
        student = self.get_student(student_id)
        if not student.active:
            raise ValidationError(f"Студент '{student_id}' деактивирован и не может сдавать работы.")
        lab = self.get_lab(lab_id)
        if not (0 <= score <= lab.max_score):
            raise ValidationError(f"Балл должен быть в диапазоне [0, {lab.max_score}].")

        existing = [
            s for s in self.submissions if s.student_id == student_id and s.lab_id == lab_id
        ]
        next_attempt = max((s.attempt for s in existing), default=0) + 1

        submission = Submission(
            student_id=student_id,
            lab_id=lab_id,
            attempt=next_attempt,
            score=score,
            comment=comment,
            status="submitted",
        )
        self.submissions.append(submission)
        return submission

    @logged_mutation
    def review_submission(
        self,
        student_id: str,
        lab_id: str,
        attempt: int,
        status: str,
        comment: str | None = None,
    ) -> Submission:
        for sub in self.submissions:
            if sub.student_id == student_id and sub.lab_id == lab_id and sub.attempt == attempt:
                sub.status = status
                if comment is not None:
                    sub.comment = comment
                sub.validate()
                return sub
        raise NotFoundError(f"Попытка №{attempt} для {student_id} / {lab_id} не найдена.")

    def iter_student_history(self, student_id: str) -> Generator[Submission, None, None]:
        self.get_student(student_id)
        for sub in self.submissions:
            if sub.student_id == student_id:
                yield sub

    # --- Статистика и отчеты ---
    def report_student(self, student_id: str) -> dict:
        student = self.get_student(student_id)
        subs = list(self.iter_student_history(student_id))
        accepted_labs = {s.lab_id for s in subs if s.status == "accepted"}

        best_by_lab: dict[str, float] = {}
        for s in subs:
            if s.lab_id not in best_by_lab or s.score > best_by_lab[s.lab_id]:
                best_by_lab[s.lab_id] = s.score

        best_score = max((s.score for s in subs), default=0.0)
        avg_score = sum(best_by_lab.values()) / len(best_by_lab) if best_by_lab else 0.0
        total_max = sum(self.labs[lid].max_score for lid in best_by_lab) if best_by_lab else 100.0
        return {
        "student": student,
        "attempts_count": len(subs),
        "completed_labs": len(accepted_labs),
        "total_labs": len(self.labs),
        "best_score": best_score,
        "avg_score": avg_score,
        "total_max": total_max,
        }

    def report_group(self) -> list[dict]:
        groups: dict[str, list[Student]] = {}
        for st in self.students.values():
            groups.setdefault(st.group, []).append(st)
        result = []
        for group_name, members in sorted(groups.items()):
            scores = [self.report_student(m.student_id)["avg_score"] for m in members]
            result.append(
            {
            "group": group_name,
            "students_count": len(members),
            "avg_score": sum(scores) / len(scores) if scores else 0.0,
            }
            )
        return result

    def report_lab(self, lab_id: str) -> dict:
        lab = self.get_lab(lab_id)
        subs = [s for s in self.submissions if s.lab_id == lab_id]
        buckets = {"0-59%": 0, "60-74%": 0, "75-89%": 0, "90-100%": 0}
        for s in subs:
            pct = (s.score / lab.max_score) * 100
            if pct < 60:
                buckets["0-59%"] += 1
            elif pct < 75:
                buckets["60-74%"] += 1
            elif pct < 90:
                buckets["75-89%"] += 1
            else:
                buckets["90-100%"] += 1
        return {
        "lab": lab,
        "attempts": len(subs),
        "avg_score": sum(s.score for s in subs) / len(subs) if subs else 0.0,
        "distribution": buckets,
        }
    def iter_missing_labs(self) -> Generator[tuple[Student, list[Lab]], None, None]:
        for st in self.students.values():
            if not st.active:
                continue
            accepted = {
            s.lab_id
            for s in self.submissions
                if s.student_id == st.student_id and s.status == "accepted"
            }
            missing = [lab for lid, lab in self.labs.items() if lid not in accepted]
            if missing:
                yield st, missing

    def report_missing(self) -> list[tuple[Student, list[Lab]]]:
        return list(self.iter_missing_labs())

    def top_students(self, n: int) -> list[tuple[Student, float]]:
        if n <= 0:
            raise ValidationError("Количество мест в рейтинге должно быть больше 0.")
        ranking: list[tuple[Student, float]] = []
        for st in self.students.values():
            best_by_lab: dict[str, float] = {}
            for s in self.submissions:
                if s.student_id == st.student_id and s.status == "accepted":
                    best_by_lab[s.lab_id] = max(best_by_lab.get(s.lab_id, 0.0), s.score)
            ranking.append((st, sum(best_by_lab.values())))
        ranking.sort(key=lambda item: (-item[1], item[0].full_name))
        if len(ranking) <= n:
            return ranking
        cutoff_score = ranking[n - 1][1]
        return [item for item in ranking if item[1] >= cutoff_score]
    # --- Импорт и экспорт ---
    def import_students_csv(self, filepath: str) -> tuple[int, list[str]]:
        path = Path(filepath)
        if not path.exists():
            raise StorageError(f"Файл '{filepath}' не найден.")
        accepted = 0
        errors: list[str] = []
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=2):
                try:
                    self.register_student(
                    student_id=row["student_id"].strip(),
                    full_name=row["full_name"].strip(),
                    group=row["group"].strip(),
                    )
                    accepted += 1
                except Exception as e:
                    errors.append(f"Строка {idx}: {e}")
        return accepted, errors
    def import_submissions_csv(self, filepath: str) -> tuple[int, list[str]]:
        path = Path(filepath)
        if not path.exists():
            raise StorageError(f"Файл '{filepath}' не найден.")
        accepted = 0
        errors: list[str] = []
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=2):
                try:
                    sub = self.submit_lab(
                    student_id=row["student_id"].strip(),
                    lab_id=row["lab_id"].strip(),
                    score=float(row["score"]),
                    comment=row.get("comment", "").strip(),
                    )
                    status = row.get("status", "").strip()
                    if status in {"accepted", "rejected"}:
                        self.review_submission(sub.student_id, sub.lab_id, sub.attempt, status)
                    accepted += 1
                except Exception as e:
                    errors.append(f"Строка {idx}: {e}")
        return accepted, errors
    def export_report(self, fmt: str, filepath: str) -> None:
        rows = []
        for st in self.students.values():
            rep = self.report_student(st.student_id)
            rows.append(
            {
            "student_id": st.student_id,
            "full_name": st.full_name,
            "group": st.group,
            "attempts": rep["attempts_count"],
            "completed_labs": rep["completed_labs"],
            "avg_score": round(rep["avg_score"], 2),
            }
            )
            if fmt == "json":
                export_to_json(filepath, rows)
            elif fmt == "csv":
                export_to_csv(filepath, rows)
            else:
                raise ValidationError("Поддерживаются форматы: json, csv.")
        # --- Анализ памяти ---
    def get_memory_stats(self) -> dict:
        tracemalloc.start()
        _ = self.report_missing()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {
            "students_count": len(self.students),
            "labs_count": len(self.labs),
            "submissions_count": len(self.submissions),
            "students_dict_bytes": sys.getsizeof(self.students),
            "labs_dict_bytes": sys.getsizeof(self.labs),
            "submissions_list_bytes": sys.getsizeof(self.submissions),
            "current_bytes": current,
            "peak_bytes": peak
            }
    def profile_memory_comparison(self) -> dict:
        tracemalloc.start()
        as_list = [s for s in self.submissions]
        list_size = sys.getsizeof(as_list)
        _, list_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tracemalloc.start()
        as_gen = (s for s in self.submissions)
        gen_size = sys.getsizeof(as_gen)
        for _ in as_gen:
            pass
        _, gen_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {
            "list_container_bytes": list_size,
            "list_peak_bytes": list_peak,
            "gen_container_bytes": gen_size,
            "gen_peak_bytes": gen_peak
            }