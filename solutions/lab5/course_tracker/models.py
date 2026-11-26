from __future__ import annotations
from collections.abc import Iterable
from datetime import datetime
from course_tracker.exceptions import ValidationError


class Student:
    def __init__(
        self,
        student_id: str,
        full_name: str,
        group: str,
        date_of_registration: datetime | None = None,
        active: bool = True,
    ):
        self.student_id = student_id
        self.full_name = full_name
        self.group = group
        self.date_of_registration = date_of_registration or datetime.now()
        self.active = active
        self.validate()

    def validate(self) -> None:
        if not self.student_id or not self.student_id.strip() or " " in self.student_id:
            raise ValidationError()
        if not self.full_name or not self.full_name.strip():
            raise ValidationError()
        if not self.group or not self.group.strip():
            raise ValidationError()

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "group": self.group,
            "date_of_registration": self.date_of_registration.isoformat(),
            "active": self.active,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Student:
        return cls(
            student_id=str(data["student_id"]),
            full_name=str(data["full_name"]),
            group=str(data["group"]),
            date_of_registration=datetime.fromisoformat(data["date_of_registration"]),
            active=bool(data["active"]),
        )


class Lab:
    def __init__(
        self,
        lab_id: str,
        title: str,
        description: str,
        max_score: float,
        deadline: datetime,
        tags: Iterable[str] | None = None,
    ):
        self.lab_id = lab_id
        self.title = title
        self.description = description
        self.max_score = float(max_score)
        self.deadline = deadline
        self.tags: set[str] = set()
        self.validate(tags)

    def validate(self, tags: Iterable[str] | None) -> None:
        if not self.lab_id or not self.lab_id.strip() or " " in self.lab_id:
            raise ValidationError()
        if not self.title or not self.title.strip():
            raise ValidationError()
        if self.max_score <= 0:
            raise ValidationError()

        if tags is not None:
            normalized = set()
            for raw_tag in tags:
                clean_tag = raw_tag.strip().lower()
                if not clean_tag:
                    raise ValidationError()
                normalized.add(clean_tag)
            self.tags = normalized

    def to_dict(self) -> dict:
        return {
            "lab_id": self.lab_id,
            "title": self.title,
            "description": self.description,
            "max_score": self.max_score,
            "deadline": self.deadline.isoformat(),
            "tags": sorted(self.tags),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Lab:
        return cls(
            lab_id=str(data["lab_id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            max_score=float(data["max_score"]),
            deadline=datetime.fromisoformat(data["deadline"]),
            tags=data.get("tags", []),
        )


class Submission:
    VALID_STATUSES = {"submitted", "accepted", "rejected"}

    def __init__(
        self,
        student_id: str,
        lab_id: str,
        attempt: int,
        score: float,
        submitted_at: datetime | None = None,
        comment: str = "",
        status: str = "submitted",
    ):
        self.student_id = student_id
        self.lab_id = lab_id
        self.attempt = attempt
        self.score = float(score)
        self.submitted_at = submitted_at or datetime.now()
        self.comment = comment
        self.status = status
        self.validate()

    def validate(self) -> None:
        if self.attempt <= 0:
            raise ValidationError()
        if self.score < 0:
            raise ValidationError()
        if self.status not in self.VALID_STATUSES:
            raise ValidationError()

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "lab_id": self.lab_id,
            "attempt": self.attempt,
            "score": self.score,
            "submitted_at": self.submitted_at.isoformat(),
            "comment": self.comment,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Submission:
        return cls(
            student_id=str(data["student_id"]),
            lab_id=str(data["lab_id"]),
            attempt=int(data["attempt"]),
            score=float(data["score"]),
            submitted_at=datetime.fromisoformat(data["submitted_at"]),
            comment=str(data.get("comment", "")),
            status=str(data.get("status", "submitted")),
        )
