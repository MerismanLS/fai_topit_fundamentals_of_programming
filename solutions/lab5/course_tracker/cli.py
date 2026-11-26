import shlex
from datetime import datetime
from course_tracker.exceptions import CourseTrackerError, ValidationError
from course_tracker.services import Course

HELP_TEXT = """Доступные команды:
  help                                              - показать эту справку
  exit                                              - сохранить состояние и выйти
  save                                              - принудительно сохранить данные
  student add <id> "<ФИО>" <группа>                 - добавить студента
  student list [id|name|group]                      - список студентов
  student show <id>                                 - карточка студента
  student deactivate <id> / activate <id>           - изменить статус активности
  student search <запрос>                           - поиск студентов
  lab add <id> "<название>" <макс_балл> <YYYY-MM-DD> [теги] ["описание"]
  lab list                                          - список лабораторных работ
  lab show <id>                                     - информация о работе
  lab search <запрос>                               - поиск работ по названию/описанию/тегам
  submit <student_id> <lab_id> <балл> ["коммент"]   - отправить попытку
  submission accept <student_id> <lab_id> <попытка> - принять попытку
  submission reject <student_id> <lab_id> <попытка> ["причина"]
  history <student_id>                              - история попыток студента
  report student <id>                               - отчет по студенту
  report group                                      - сводный отчет по группам
  report lab <id>                                   - статистика по лабораторной работе
  report missing                                    - список несданных работ
  top <N>                                           - рейтинг топ-N студентов
  import students <путь.csv>                        - импорт студентов из CSV
  import submissions <путь.csv>                     - импорт попыток из CSV
  export json <путь.json> / export csv <путь.csv>   - экспорт отчета
  snapshot create / snapshot restore                - создать или восстановить снимок
  undo                                              - отменить последнее изменение
  memory / memory profile                           - статистика и профилирование памяти"""


class CourseTrackerCLI:
    def __init__(self, course: Course):
        self.course = course

    def run(self) -> None:
        self.course.load_state()
        print("CourseTracker 1.0")
        print("Введите help для просмотра команд.\n")

        while True:
            try:
                raw_input = input("course-tracker> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                self.course.save_state()
                print("Работа завершена.")
                break

            if not raw_input:
                continue

            try:
                args = shlex.split(raw_input)
            except ValueError as e:
                print(f"Ошибка синтаксиса кавычек: {e}")
                continue

            try:
                should_exit = self.dispatch(args)
                if should_exit:
                    break
            except CourseTrackerError as e:
                print(f"Ошибка: {e}")
            except (IndexError, ValueError) as e:
                print(f"Некорректные аргументы команды ({e}). Введите help для справки.")

    def dispatch(self, args: list[str]) -> bool:
        cmd = args[0].lower()
        match cmd:
            case "help":
                print(HELP_TEXT)
            case "exit":
                self.course.save_state()
                print("Работа завершена.")
                return True
            case "save":
                self.course.save_state()
                print("Данные сохранены.")
            case "student":
                self._handle_student(args[1:])
            case "lab":
                self._handle_lab(args[1:])
            case "submit":
                if len(args) < 4:
                    raise ValidationError("Формат: submit <student_id> <lab_id> <балл> [комментарий]")
                comment = args[4] if len(args) > 4 else ""
                sub = self.course.submit_lab(args[1], args[2], float(args[3]), comment)
                print(f"Сохранена попытка № {sub.attempt}.")
            case "submission":
                self._handle_submission(args[1:])
            case "history":
                subs = list(self.course.iter_student_history(args[1]))
                if not subs:
                    print("Попыток не найдено.")
                for s in subs:
                    print(
                        f"[{s.submitted_at:%Y-%m-%d %H:%M}] {s.lab_id} | "
                        f"Попытка #{s.attempt}: {s.score} ({s.status}) — {s.comment}"
                    )
            case "report":
                self._handle_report(args[1:])
            case "top":
                n = int(args[1])
                leaders = self.course.top_students(n)
                for idx, (st, total) in enumerate(leaders, start=1):
                    print(f"{idx}. {st.full_name} ({st.student_id}, {st.group}) — {total:.2f} б.")
            case "import":
                self._handle_import(args[1:])
            case "export":
                if len(args) < 3:
                    raise ValidationError("Формат: export <json|csv> <путь>")
                self.course.export_report(args[1].lower(), args[2])
                print(f"Отчет экспортирован в {args[2]}.")
            case "snapshot":
                self._handle_snapshot(args[1:])
            case "undo":
                self.course.undo()
                print("Последнее изменение отменено.")
            case "memory":
                self._handle_memory(args[1:])
            case _:
                print("Неизвестная команда. Введите help для списка команд.")
        return False

    def _handle_student(self, args: list[str]) -> None:
        if not args:
            raise ValidationError("Укажите подкоманду для student.")
        match args[0]:
            case "add":
                st = self.course.register_student(args[1], args[2], args[3])
                print(f"Студент {st.student_id} добавлен.")
            case "list":
                sort_by = args[1] if len(args) > 1 else "id"
                for st in self.course.list_students(sort_by):
                    status = "активен" if st.active else "деактивирован"
                    print(f"{st.student_id} | {st.full_name} | {st.group} | {status}")
            case "show":
                st = self.course.get_student(args[1])
                print(
                    f"ID: {st.student_id}\nФИО: {st.full_name}\nГруппа: {st.group}\n"
                    f"Регистрация: {st.date_of_registration:%Y-%m-%d}\nАктивен: {st.active}"
                )
            case "deactivate":
                self.course.set_student_active(args[1], False)
                print(f"Студент {args[1]} деактивирован.")
            case "activate":
                self.course.set_student_active(args[1], True)
                print(f"Студент {args[1]} активирован.")
            case "search":
                found = self.course.search_students(args[1])
                for st in found:
                    print(f"{st.student_id} | {st.full_name} | {st.group}")
                if not found:
                    print("Ничего не найдено.")
            case _:
                raise ValidationError("Неизвестная подкоманда student.")

    def _handle_lab(self, args: list[str]) -> None:
        if not args:
            raise ValidationError("Укажите подкоманду для lab.")
        match args[0]:
            case "add":
                tags = args[5].split(",") if len(args) > 5 and args[5] else []
                desc = args[6] if len(args) > 6 else ""
                lab = self.course.create_lab(
                    lab_id=args[1],
                    title=args[2],
                    max_score=float(args[3]),
                    deadline=datetime.fromisoformat(args[4]),
                    tags=tags,
                    description=desc,
                )
                print(f"Лабораторная работа {lab.lab_id} добавлена.")
            case "list":
                for lab in self.course.list_labs():
                    print(
                        f"{lab.lab_id} | {lab.title} | Макс: {lab.max_score} | "
                        f"Срок: {lab.deadline:%Y-%m-%d} | Теги: {', '.join(sorted(lab.tags))}"
                    )
            case "show":
                lab = self.course.get_lab(args[1])
                print(
                    f"ID: {lab.lab_id}\nНазвание: {lab.title}\nОписание: {lab.description}\n"
                    f"Макс. балл: {lab.max_score}\nДедлайн: {lab.deadline:%Y-%m-%d}\n"
                    f"Теги: {', '.join(sorted(lab.tags))}"
                )
            case "search":
                found = self.course.search_labs(args[1])
                for lab in found:
                    print(f"{lab.lab_id} | {lab.title} | Теги: {', '.join(sorted(lab.tags))}")
                if not found:
                    print("Ничего не найдено.")
            case _:
                raise ValidationError("Неизвестная подкоманда lab.")

    def _handle_submission(self, args: list[str]) -> None:
        if len(args) < 4:
            raise ValidationError("Укажите: submission <accept|reject> <student_id> <lab_id> <попытка>")
        action = args[0]
        if action == "accept":
            self.course.review_submission(args[1], args[2], int(args[3]), "accepted")
            print("Попытка принята.")
        elif action == "reject":
            reason = args[4] if len(args) > 4 else ""
            self.course.review_submission(args[1], args[2], int(args[3]), "rejected", reason)
            print("Попытка отклонена.")
        else:
            raise ValidationError("Доступны только действия accept или reject.")

    def _handle_report(self, args: list[str]) -> None:
        if not args:
            raise ValidationError("Укажите тип отчета: student, group, lab, missing.")
        match args[0]:
            case "student":
                rep = self.course.report_student(args[1])
                print(
                f"{rep['student'].full_name}\n"
                f"Выполнено работ: {rep['completed_labs']}/{rep['total_labs']}\n"
                f"Попыток: {rep['attempts_count']}\n"
                f"Лучший результат: {rep['best_score']:.2f}\n"
                f"Средний результат: {rep['avg_score']:.2f}"
                )
            case "group":
                for row in self.course.report_group():
                    print(
                    f"Группа {row['group']}: студентов {row['students_count']}, "
                    f"средний балл {row['avg_score']:.2f}"
                    )
            case "lab":
                rep = self.course.report_lab(args[1])
                print(
                f"{rep['lab'].title} (попыток: {rep['attempts']}, "
                f"средний балл: {rep['avg_score']:.2f})\n"
                f"Распределение: {rep['distribution']}"
                )
            case "missing":
                missing = self.course.report_missing()
                if not missing:
                    print("Все активные студенты сдали все работы.")
                for st, labs in missing:
                    lab_ids = ", ".join(l.lab_id for l in labs)
                    print(f"{st.full_name} ({st.student_id}): не сданы [{lab_ids}]")
            case _:
                raise ValidationError("Неизвестный тип отчета.")
    def _handle_import(self, args: list[str]) -> None:
        if len(args) < 2:
            raise ValidationError("Формат: import <students|submissions> <путь>")
        if args[0] == "students":
            ok, errs = self.course.import_students_csv(args[1])
        elif args[0] == "submissions":
            ok, errs = self.course.import_submissions_csv(args[1])
        else:
            raise ValidationError("Импорт поддерживается для students и submissions.")
        print(f"Принято записей: {ok}. Отклонено: {len(errs)}.")
        for err in errs:
            print(f"  - {err}")
    def _handle_snapshot(self, args: list[str]) -> None:
        if not args or args[0] not in {"create", "restore"}:
            raise ValidationError("Используйте: snapshot create или snapshot restore")
        if args[0] == "create":
            self.course.create_snapshot()
            print("Снимок состояния создан.")
        else:
            self.course.restore_snapshot()
            print("Состояние восстановлено из снимка.")
    def _handle_memory(self, args: list[str]) -> None:
        stats = self.course.get_memory_stats()
        print(
        f"Студенты: {stats['students_count']}\n"
        f"Работы: {stats['labs_count']}\n"
        f"Попытки: {stats['submissions_count']}\n"
        f"Размер коллекций (sys.getsizeof): dict(students)={stats['students_dict_bytes']} Б, "
        f"dict(labs)={stats['labs_dict_bytes']} Б, list(submissions)={stats['submissions_list_bytes']} Б\n"
        f"Текущая память (tracemalloc): {stats['current_bytes']} Б\n"
        f"Пиковая память (tracemalloc): {stats['peak_bytes']} Б"
        )
        if args and args[0] == "profile":
            prof = self.course.profile_memory_comparison()
            print(
            f"\nСравнение (список vs генератор):\n"
            f"Список: контейнер {prof['list_container_bytes']} Б, пик {prof['list_peak_bytes']} Б\n"
            f"Генератор: объект {prof['gen_container_bytes']} Б, пик {prof['gen_peak_bytes']} Б"
            )