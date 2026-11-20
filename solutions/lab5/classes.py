import json
from datetime import datetime
from collections.abc import Iterable

class Student:
    def __init__(self, id: str, full_name: str, group: str, date_of_registration: datetime = datetime.now(), activity: bool = True):
        self.id = id
        self.full_name = full_name
        self.group = group
        self.date_of_registration = date_of_registration
        self.activity = activity
        self.validation()

    def validation(self):
        check_id = self.id.strip() != '' and " " not in self.id
        check_name = self.full_name.strip() != ''

        if not check_id:
            raise ValueError('Некорректный идентификатор')
        if not check_name:
            raise ValueError('Некорректное имя')

class StudentsStorage:
    def __init__(self):
        self.storage: dict[str, Student] = {}

    def add(self, student: Student) -> None:
        if student.id in self.storage:
            raise ValueError('Студент с таким идентификатором уже существует')
        else:
            self.storage[student.id] = student

class Lab:
    def __init__(self, id: str, name: str, description: str, max_res: int, deadline: datetime, tags: Iterable[str] | None = None):
        self.id = id
        self.name = name
        self.description = description
        self.max_res = max_res
        self.deadline = deadline
        self.tags = set()

        self.validation(tags)

    def validation(self, tags: Iterable[str]):
        check_id = self.id.strip() != ''
        check_name = self.name.strip() != ''
        check_res = self.max_res > 0

        if not check_id:
            raise ValueError('Некорректный идентификатор')

        if not check_name:
            raise ValueError('Некорректное имя')

        if not check_res:
            raise ValueError('Максимальный результат должен быть больше нуля')

        if tags is not None:
            tags_list = list(tags)
            if any(not tag.strip() for tag in tags_list):
                raise ValueError("Теги не должны содержать пустых значений")
            unique_tags = set(tags_list)
            if len(tags_list) != len(unique_tags):
                raise ValueError("Теги не должны содержать повторов")
            self.tags = unique_tags

class LabsStorage:
    def __init__(self):
        self.storage: dict[str, Lab] = {}

    def add(self, lab: Lab) -> None:
        if lab.id in self.storage:
            raise ValueError('Лабораторная с таким идентификатором уже существует')
        else:
            self.storage[lab.id] = lab

class Submission:
    def __init__(
            self,
            student_id: str,
            lab_id: str,
            attempt: int,
            result: int,
            submitted: datetime,
            comment: str,
            status: str
    ):
        self.student_id = student_id
        self.lab_id = lab_id
        self.attempt = attempt
        self.result = result
        self.submitted = submitted
        self.comment = comment
        self.status = status

        self.validation()

    def validation(self):
        check_attempt = self.attempt > 0
        check_status = self.status in ['submitted', 'accepted', 'rejected']

        if not check_attempt:
            raise ValueError('Недопустимый номер попутки')

        if not check_status:
            raise ValueError('Некорректный статус попытки')

class SubmissionStorage:
    def __init__(self, students_storage: StudentsStorage, labs_storage: LabsStorage):
        self.students_storage = students_storage
        self.labs_storage = labs_storage
        self.submissions: list[Submission] = []

    def submit(
            self,
            student_id: str,
            lab_id: str,
            result: int,
            attempt: int = 0,
            comment: str = "",
            status: str = "submitted",
            submitted: datetime | None = None,
    ) -> Submission:
        if student_id not in self.students_storage.storage:
            raise ValueError(f"Студент '{student_id}' не найден")

        lab = self.labs_storage.storage.get(lab_id)
        if lab is None:
            raise ValueError(f"Лабораторная работа '{lab_id}' не найдена")

        if not (0 <= result <= lab.max_res):
            raise ValueError(f"Результат должен быть в диапазоне от 0 до {lab.max_res}")


        previous_attempts = [
            s for s in self.submissions
            if s.student_id == student_id and s.lab_id == lab_id
        ]
        next_attempt = len(previous_attempts) + 1

        # 4. Создаем и сохраняем попытку
        submission = Submission(
            student_id=student_id,
            lab_id=lab_id,
            attempt=next_attempt,
            result=result,
            submitted=submitted,
            comment=comment,
            status=status,
        )
        self.submissions.append(submission)
        return submission

class Course:
    def __init__(self):
        self.students = StudentsStorage()
        self.labs = LabsStorage()
        self.submissions = SubmissionStorage(self.students, self.labs)

    def read_saved_data(self):
        with open("/data/saved_students.json", mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for item in data:
            student = Student(
                id=str(item['id']),
                full_name=item['full_name'],
                group=item['group'],
                date_of_registration=datetime.fromisoformat(item['date_of_registration']),
                activity=bool(item['activity'])
            )
            self.students.add(student)

        with open("/data/saved_labs.json", mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for item in data:
            lab = Lab(
                id=item['id'],
                name=item['name'],
                description=item['description'],
                max_res=item['max_res'],
                deadline=datetime.fromisoformat(item['deadline']),
                tags=item["tags"]
            )
            self.labs.add(lab)

        with open("/data/saved_subs.json", mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        for item in data:
            self.submissions.submit(
                student_id=item['student_id'],
                lab_id=item['lab_id'],
                attempt=item['attempt'],
                result=item['result'],
                submitted=datetime.fromisoformat(item['submitted']),
                comment=item['comment'],
                status=item['status']
            )

    def register_student(self, id: str, full_name: str, group: str) -> Student:
        student = Student(id=id, full_name=full_name, group=group)
        self.students.add(student)
        return student

    def create_lab(
        self,
        id: str,
        name: str,
        description: str,
        max_res: int,
        deadline: datetime,
        tags: Iterable[str] | None = None,
    ) -> Lab:
        lab = Lab(
            id=id,
            name=name,
            description=description,
            max_res=max_res,
            deadline=deadline,
            tags=tags,
        )
        self.labs.add(lab)
        return lab

    def submit_lab(
        self,
        student_id: str,
        lab_id: str,
        result: int,
        comment: str = "",
        status: str = "submitted",
        submitted: datetime | None = None,
    ) -> Submission:
        return self.submissions.submit(
            student_id=student_id,
            lab_id=lab_id,
            result=result,
            comment=comment,
            status=status,
            submitted=submitted or datetime.now(),
        )

    def get_student(self, student_id: str) -> Student | None:
        return self.students.storage.get(student_id)

    def get_lab(self, lab_id: str) -> Lab | None:
        return self.labs.storage.get(lab_id)

    def get_student_submissions(self, student_id: str) -> list[Submission]:
        return [s for s in self.submissions.submissions if s.student_id == student_id]
