from abc import abstractmethod, ABC
from datetime import datetime

class CourseEvent(ABC):
    def __init__(self, student_id, created_at: datetime):
        self._student_id = student_id
        self.created_at = created_at

    @property
    @abstractmethod
    def student_id(self):
        return self._student_id

    @abstractmethod
    def describe(self):
        pass

class SubmissionEvent(CourseEvent, ABC):
    def __init__(self, student_id, laboratory_id, attempt, score, created_at):
        super().__init__(student_id, created_at)
        self.laboratory_id = laboratory_id
        self.attempt = attempt
        self.score = score

    @property
    def student_id(self):
        return self._student_id

    def describe(self):
        return (
            f"[{self.created_at:%Y-%m-%d %H:%M}] Сдача работы: студент {self.student_id}, "
            f"лабораторная '{self.laboratory_id}' (попытка №{self.attempt}, балл: {self.score})"
        )

class AttendanceEvent(CourseEvent, ABC):
    def __init__(self, student_id, created_at, lesson, status):
        super().__init__(student_id, created_at)
        self.lesson = lesson
        self.status = status

    @property
    def student_id(self):
        return self._student_id

    def describe(self):
        return (
            f"[{self.created_at:%Y-%m-%d %H:%M}] Посещаемость: студент {self.student_id} — "
            f"{self.status} на занятии «{self.lesson}»"
        )

class CommentEvent(CourseEvent, ABC):
    def __init__(self, student_id, created_at, comment):
        super().__init__(student_id, created_at)
        self.comment = comment

    @property
    def student_id(self):
        return self._student_id

    def describe(self):
        return (
            f"[{self.created_at:%Y-%m-%d %H:%M}] Комментарий "
            f"для студента {self.student_id}: '{self.comment}'"
        )

# практическое расширение
class DeadlineEvent(CourseEvent, ABC):
    def __init__(self, student_id, deadline):
        super().__init__(student_id, deadline)
        self.deadline = deadline

    @property
    def student_id(self):
        return self._student_id

    def describe(self):
        return (
            f"=== Дедлайн {self.deadline:%Y-%m-%d %H:%M}!!! ==="
        )
# практическое расширение


class CourseJournal:
    def __init__(self):
        self._events: list[CourseEvent] = []

    def add_event(self, event: CourseEvent):
        self._events.append(event)

    def __len__(self) -> int:
        return len(self._events)

    def __getitem__(self, index: int | slice):
        return self._events[index]

    def __str__(self) -> str:
        if not self._events:
            return f"Журнал курса пуст."
        lines = [f"Журнал курса:"]
        for i, event in enumerate(self._events, start=1):
            lines.append(f"  {i}. {event.describe()}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"CourseJournal(events_count={len(self)})"

    def events_for_student(self, student_id: str):
        for event in self._events:
            if event.student_id == student_id:
                yield event

    def events_by_type(self, event_type):
        for event in self._events:
            if isinstance(event, event_type):
                yield event

    def summary(self):
        by_type = {}
        students = set()
        for event in self._events:
            event_name = type(event).__name__
            by_type[event_name] = by_type.get(event_name, 0) + 1
            students.add(event.student_id)
        return {
            "total_events": len(self._events),
            "students_count": len(students),
            "by_type": by_type,
        }

def render_timeline(events):
    lines = []
    for event in events:
        lines.append(event.describe())
    return "\n".join(lines)

class ScoreView:
    def __init__(self, events):
        self._events = events

    def __iter__(self):
        for event in self._events:
            if isinstance(event, SubmissionEvent):
                yield event.score

class FilteredJournalView:
    def __init__(self, events, predicate):
        self._events = events
        self.predicate = predicate

    def __iter__(self):
        for event in self._events:
            if self.predicate(event):
                yield event


if __name__ == "__main__":
    journal = CourseJournal()

    students = ["st_01", "st_02", "st_03"]
    now = datetime.now()

    events_data = [
        AttendanceEvent("st_01", now, "Введение в ООП", status="присутствовал"),
        AttendanceEvent("st_02", now, "Введение в ООП", status="присутствовал"),
        AttendanceEvent("st_03", now, "Введение в ООП", status="отсутствовал"),
        SubmissionEvent("st_01", "lab_1", attempt=1, score=68.0, created_at=now),
        CommentEvent("st_01", now, "Нужно исправить обработку исключений"),
        SubmissionEvent("st_01", "lab_1", attempt=2, score=94.0, created_at=now),
        SubmissionEvent("st_02", "lab_1", attempt=1, score=88.5, created_at=now),
        AttendanceEvent("st_01", now, "Наследование и полиморфизм", status="присутствовал"),
        AttendanceEvent("st_02", now, "Наследование и полиморфизм", status="присутствовал"),
        SubmissionEvent("st_03", "lab_1", attempt=1, score=75.0, created_at=now),
        CommentEvent("st_02", now, "Отличное оформление кода"),
        SubmissionEvent("st_01", "lab_2", attempt=1, score=98.0, created_at=now),
    ]

    for ev in events_data:
        journal.add_event(ev)

    print(f"Всего событий в журнале: {len(journal)}")
    print("Сводка журнала:", journal.summary())

    print("\n--- События студента st_01 ---")
    for ev in journal.events_for_student("st_01"):
        print(ev.describe())

    print("\n--- Все комментарии на курсе ---")
    for ev in journal.events_by_type(CommentEvent):
        print(ev.describe())

    print("\n--- Срез журнала journal[3:7] ---")
    for ev in journal[3:7]:
        print(ev.describe())

    print("\n--- Полная временная шкала ---")
    print(render_timeline(journal))

    scores = ScoreView(journal)

    first_pass = list(scores)
    second_pass = list(scores)

    avg_score = sum(scores) / len(first_pass)
    max_score = max(scores)
    min_score = min(scores)

    print("\n--- Статистика по ScoreView ---")
    print(f"Все оценки (1-й обход): {first_pass}")
    print(f"Все оценки (2-й обход): {second_pass}")
    print(f"Средний балл: {avg_score:.2f} | Мин: {min_score} | Макс: {max_score}")

    # --- Демонстрация практического расширения ---
    journal.add_event(
        DeadlineEvent("st_01",  datetime(2026, 11, 20, 23, 59))
    )
    journal.add_event(
        DeadlineEvent("st_02",  datetime(2026, 11, 20, 23, 59))
    )

    print("\n--- Обновленная временная шкала (с DeadlineEvent) ---")
    print(render_timeline(journal))

    def is_excellent_submission(event: CourseEvent) -> bool:
        return isinstance(event, SubmissionEvent) and event.score >= 90.0

    excellent_view = FilteredJournalView(journal, is_excellent_submission)

    print("\n--- Отличные сдачи (именованная функция) ---")
    for ev in excellent_view:
        print(f"  {ev.describe()}")

    st02_view = FilteredJournalView(journal, lambda ev: ev.student_id == "st_02")

    first_run = list(st02_view)
    second_run = list(st02_view)
    assert first_run == second_run, "Повторный обход должен возвращать те же события"

    print(f"\n--- События st_02 через lambda (повторный обход: {len(second_run)} шт.) ---")
    print(render_timeline(st02_view))

