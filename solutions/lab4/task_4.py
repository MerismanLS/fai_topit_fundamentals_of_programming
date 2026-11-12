from dataclasses import dataclass
from functools import total_ordering


@total_ordering
@dataclass(order=False, eq=False)
class Submission:
    student_id: str
    laboratory_id: str
    attempt: int
    score: float
    comment: str = ""

    def __post_init__(self):
        if self.student_id == "":
            raise ValueError("Student id cannot be empty")
        if self.laboratory_id == "":
            raise ValueError("Laboratory id cannot be empty")
        if not (0 <= self.score <= 100):
            raise ValueError("Attempt must be between 0 and 100")

    def _key(self):
        return (
        self.attempt,
        self.score
        )

    def __eq__(self, other: object) -> bool:
        return self._key() == other._key()

    def __lt__(self, other: object) -> bool:
        return self._key() < self._key()

class Student:
    def __init__(self, student_id: str, student_name: str):
        self.student_id = student_id
        self.student_name = student_name
        self._labs_list = []

    @staticmethod
    def is_valid_id(student_id: str) -> bool:
        return isinstance(student_id, str) and student_id != ""

    @classmethod
    def from_full_name(cls, student_id, full_name):
        if not (cls.is_valid_id(student_id)):
            raise ValueError("Полное имя не может быть пустым")
        normalized_name = " ".join(full_name.split())
        return cls(student_id, normalized_name)

    def add_submission(self, submission: Submission):
        self._labs_list.append(submission)

    @property
    def submissions(self):
        return self._labs_list

    @property
    def average_score(self):
        if len(self._labs_list) != 0:
            return sum(self._labs_list) / len(self._labs_list)
        else:
            return 0

    def best_score(self, laboratory_id: str):
        exact_labs = [sub.score for sub in self._labs_list if sub.laboratory_id == laboratory_id]
        return max(exact_labs)

    def sorted_submissions(self) -> list[Submission]:
        return sorted(self._labs_list, key=lambda sub: (sub.attempt, sub.score))

    def __len__(self):
        return len(self._labs_list)

    def __iter__(self):
        return iter(self._labs_list)

    def __str__(self):
        return f"Студент {self.student_name}"

    def __repr__(self):
        text = (f"Студент: {self.student_name}\n"
                f"ID студента: {self.student_id}\n"
                f"Работы студента: {self.submissions}")
        return text

class Course:
    def __init__(self):
        self.students = {}

    def add_student(self, student: Student):
        if student.student_id not in self.students:
            self.students[student.student_id] = student

    def get_student(self, student_id: str):
        return self.students[student_id]

    def submit(self, submission: Submission):
        student = self.get_student(submission.student_id)
        student.add_submission(submission)

    def top_students(self, limit: int = 3):
        score = sorted(self.students.values(), key=lambda student: student.average_score, reverse=True)[:limit]
        return score

    def __contains__(self, student_id):
        return student_id in self.students

    def __len__(self):
        return len(self.students)

    def __iter__(self):
        return iter(self.students_ids)