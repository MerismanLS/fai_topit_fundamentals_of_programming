# Исходные данные из задания
students = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61],
}

# --- Обязательные функции ---

def mean(values: list[int | float]) -> float:
    """Вычисляет среднее значение списка. Для пустого списка возвращает 0.0."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def minimum(values: list[int | float]) -> int | float:
    """Находит минимум без использования встроенной функции min()."""
    if not values:
        return 0
    current_min = values[0]
    for val in values:
        if val < current_min:
            current_min = val
    return current_min


def maximum(values: list[int | float]) -> int | float:
    """Находит максимум без использования встроенной функции max()."""
    if not values:
        return 0
    current_max = values[0]
    for val in values:
        if val > current_max:
            current_max = val
    return current_max


def classify(score: float) -> str:
    """Возвращает текстовую категорию в зависимости от среднего балла."""
    if score == 0.0:
        return "Недостаточно данных"
    elif score >= 90:
        return "Отлично"
    elif score >= 75:
        return "Хорошо"
    elif score >= 60:
        return "Удовлетворительно"
    else:
        return "Неудовлетворительно"


def student_summary(name: str, results: list[int]) -> dict:
    """Формирует словарь с итогами для одного студента."""
    avg_score = mean(results)
    return {
        "name": name,
        "mean": avg_score,
        "min": minimum(results),
        "max": maximum(results),
        "category": classify(avg_score)
    }


def group_summary(students_data: dict[str, list[int]]) -> dict:
    """Вычисляет общую статистику группы (общий средний балл и распределение по категориям)."""
    if not students_data:
        return {"group_mean": 0.0, "categories_count": {}}

    all_means = []
    categories_count = {
        "Отлично": 0, "Хорошо": 0, "Удовлетворительно": 0,
        "Неудовлетворительно": 0, "Недостаточно данных": 0
    }

    for name, results in students_data.items():
        summary = student_summary(name, results)
        all_means.append(summary["mean"])
        categories_count[summary["category"]] += 1

    return {
        "group_mean": mean(all_means),
        "categories_count": {k: v for k, v in categories_count.items() if v > 0}  # Убираем пустые для красоты
    }


def find_top_students(students_data: dict[str, list[int]]) -> list[str]:
    """Возвращает список студентов с наибольшим средним результатом (лидеров)."""
    if not students_data:
        return []

    summaries = [student_summary(name, res) for name, res in students_data.items()]

    # Находим максимальный средний балл вручную
    max_mean = summaries[0]["mean"]
    for s in summaries:
        if s["mean"] > max_mean:
            max_mean = s["mean"]

    # Собираем всех, у кого балл равен максимальному (на случай ничьей)
    return [s["name"] for s in summaries if s["mean"] == max_mean]


def format_report(student_data: dict[str, list[int]], group_data: dict) -> str:
    """Формирует красивый итоговый текстовый отчет."""
    if not student_data:
        return "Отчет: Данные группы отсутствуют.\n"

    # Создаем рейтинг (сортируем по среднему баллу без изменения исходного словаря)
    summaries = [student_summary(name, res) for name, res in student_data.items()]
    # Классическая сортировка выбором (Selection Sort) для рейтинга по убыванию среднего балла
    n = len(summaries)
    for i in range(n - 1):
        max_idx = i
        for j in range(i + 1, n):
            if summaries[j]["mean"] > summaries[max_idx]["mean"]:
                max_idx = j
        summaries[i], summaries[max_idx] = summaries[max_idx], summaries[i]

    report = "=== ОТЧЕТ ОБ УСПЕВАЕМОСТИ ГРУППЫ ===\n\n"
    report += "Рейтинг студентов:\n"
    for idx, s in enumerate(summaries, 1):
        report += f"{idx}. {s['name']}: Ср.балл = {s['mean']:.2f}, Мин = {s['min']}, Макс = {s['max']} ({s['category']})\n"

    report += f"\nОбщий средний балл группы: {group_data['group_mean']:.2f}\n"

    report += "\nРаспределение по категориям:\n"
    for cat, count in group_data["categories_count"].items():
        report += f" - {cat}: {count} чел.\n"

    leaders = find_top_students(student_data)
    report += f"\nЛидер(ы) группы: {', '.join(leaders)}\n"
    return report

# =====================================================================

print("Проверки")

# Сценарий 1: Обычный набор данных
data_1 = {
    "Анна": [78, 91, 84, 88],
    "Борис": [60, 72, 68],
    "Дарья": [95, 93, 97, 90],
    "Илья": [55, 61]
}
if find_top_students(data_1) == ["Дарья"]:
    print(" -> Сценарий 1 (Обычные данные): Успешно")

# Сценарий 2: Один студент
data_2 = {"Игорь": [10, 24, 52]}
if find_top_students(data_2) == ["Игорь"]:
    print(" -> Сценарий 2 (Один студент): Успешно")

# Сценарий 3: Несколько лидеров (ничья)
data_3 = {
    "Маша": [80, 90],
    "Павел": [95, 75],
    "Олег": [60, 70]
}
if sorted(find_top_students(data_3)) == ["Маша", "Павел"]:
    print(" -> Сценарий 3 (Несколько лидеров): Успешно")

# Сценарий 4: Пустая группа
data_4 = {}
if find_top_students(data_4) == [] and group_summary(data_4)["group_mean"] == 0.0:
    print(" -> Сценарий 4 (Пустая группа): Успешно")

# Сценарий 5: Студент без результатов
data_5 = {
    "Анна": [86, 13],
    "Семён": []
}
semen = student_summary("Семён", [])
if semen["mean"] == 0.0 and semen["category"] == "Недостаточно данных":
    print(" -> Сценарий 5 (Студент без результатов): Успешно")

# Сценарий 6: Граничные значения категорий
if (classify(90.0) == "Отлично" and
    classify(89.9) == "Хорошо" and
    classify(75.0) == "Хорошо" and
    classify(60.0) == "Удовлетворительно"):
    print(" -> Сценарий 6 (Граничные значения): Успешно")

print("\nВсе сценарии успешно проверены")