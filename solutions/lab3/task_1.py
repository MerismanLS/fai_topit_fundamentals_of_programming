def classifying(data) -> tuple:
    # result = int(input("Введите результат студента от 0 до 100: "))
    # if not (0 <= result <= 100): return "ошибка в результате студента"
    # type_of_work = input("Введите тип работы (exam, project, practice): ")
    # if type_of_work not in ["exam", "project", "practice"]: return "ошибка в типе работы"
    # count_missed = int(input("Введите количество пропущенных занятий от 0 до 5: "))
    # if not (0 <= count_missed <= 5): return "ошибка в количестве пропущенных занятий"

    result = data[0]
    if not (0 <= result <= 100): return ("ошибка в результате студента", "", "", 0)

    type_of_work = data[1]
    if type_of_work not in ["exam", "project", "practice"]: return ("ошибка в типе работы", "", "", 0)

    count_missed = data[2]
    if not (0 <= count_missed <= 5): return ("ошибка в количестве пропущенных занятий", "", "", 0)

    student_level = ""

    levels = ["отличный", "хороший", "удовлетворительный", "недостаточный"]

    match result:
        case num if num >= 90:
            student_level = levels[0]
            if count_missed > 3:
                student_level = levels[1]
        case num if num >= 75:
            student_level = levels[1]
            if count_missed > 3:
                student_level = levels[2]
        case num if num >= 60:
            student_level = levels[2]
        case _:
            student_level = levels[3]

    type_of_work_in_russian = ""

    types = ["экзаменационная", "проектная", "практическая", "неизвестная"]

    match type_of_work:
        case "exam":
            type_of_work_in_russian = types[0]
        case "project":
            type_of_work_in_russian = types[1]
        case "practice":
            type_of_work_in_russian = types[2]
        case _:
            type_of_work_in_russian = types[3]

    final_text = (
        "===========================\n"
        f"Набрано баллов: {result}\n"
        f"Тип работы: {type_of_work_in_russian}\n"
        f"Пропущено занятий: {count_missed}\n"
        f"Итоговый уровень: {student_level}\n"
        "==========================="
    )

    return (final_text, student_level, type_of_work_in_russian, count_missed)

data = [
    (0, "exam", 3),
    (59, "practice", 2),
    (60, "exam", 4),
    (74, "project", 0),
    (75, "practice", 1),
    (89, "exam", 5),
    (90, "practice", 2),
    (100, "practice", 0),
    (83, "practice", 1),
    (20, "practice", 5),
    (-3, "not_working", -1)
]

result_levels = {
    "отличный": 0,
    "хороший": 0,
    "удовлетворительный": 0,
    "недостаточный": 0
}

result_works = {
    "экзаменационная": 0,
    "проектная": 0,
    "практическая": 0,
    "неизвестная": 0
}

result_missed = 0

for elem in data:
    result = classifying(elem)
    print(result[0])

    if result[1] != "":
        result_levels[result[1]] += 1
        result_works[result[2]] += 1
        result_missed += result[3]

final_report = (
        "\n\n\n"
        "Сводка\n"
        "===========================\n"
        f"Количество учеников по уровням\n"
        f"Отличный уровень: {result_levels["отличный"]}\n"
        f"Хороший уровень: {result_levels["хороший"]}\n"
        f"Удовлетворительный уровень: {result_levels["удовлетворительный"]}\n"
        f"Недостаточный уровень: {result_levels["недостаточный"]}\n"
        "===========================\n"
        f"Количество работ\n"
        f"Экзаменационная: {result_works["экзаменационная"]}\n"
        f"Проектная: {result_works["проектная"]}\n"
        f"Практическая: {result_works["практическая"]}\n"
        f"Неизвестная: {result_works["неизвестная"]}\n"
        "===========================\n"
        f"Всего пропущено уроков: {result_missed}\n"
        "==========================="
    )

print(final_report)

# while True:
#     text = classifying()
#     print(text)