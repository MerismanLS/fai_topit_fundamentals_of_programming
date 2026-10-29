def arithmetic_mean(values: list[float]) -> float:
    if len(values) == 0:
        return 0.0
    return sum(values) / len(values)
    """Возвращает среднее арифметическое непустого списка."""


def normalize_name(name: str) -> str:
    if not name.strip():
        return ""

    normalized_words = []

    for word in name.split():
        parts = [part.capitalize() for part in word.split("-")]
        normalized_words.append("-".join(parts))

    return " ".join(normalized_words)


def build_report(
    student: str,
    results: list[int],
    *,
    precision: int = 2,
    prefix: str = "Результат",
) -> str:
    """Формирует строковый отчет о результатах студента."""
    if not student.strip() or not results:
        return f"{prefix}: нет данных"

    student_name = normalize_name(student)
    mean = arithmetic_mean([float(result) for result in results])
    results_text = ", ".join(str(result) for result in results)

    return (
        f"{prefix}: {student_name} — результаты: {results_text}; "
        f"средний балл: {mean:.{precision}f}")


def collect_tags(*tags: str, lowercase: bool = True) -> tuple[str, ...]:
    """Возвращает очищенные теги без пустых значений и повторов."""
    result = []
    for tag in tags:
        cleaned = tag.strip()
        if cleaned:
            if lowercase:
                cleaned = cleaned.lower()

            if cleaned not in result:
                result.append(cleaned)

    return tuple(result)



if __name__ == "__main__":
    # Проверки arithmetic_mean
    # -----------------------------------------------------------------------
    values = [3.0, 1.0, 2.0]
    values_before = values.copy()

    assert arithmetic_mean(values) == 2.0
    assert values == values_before
    assert arithmetic_mean([]) == 0.0

    # Проверки normalize_name
    # -----------------------------------------------------------------------
    assert normalize_name("  Anna   smirnova ") == "Anna Smirnova"
    assert normalize_name("Anna-MARIA petrova-Vodkina") == "Anna-Maria Petrova-Vodkina"
    assert normalize_name("   ") == ""

    # Проверки build_report
    # -----------------------------------------------------------------------
    results = [5, 4, 5]
    results_before = results.copy()

    assert build_report("  Anna   SMIRNOVA ", results) == (
        "Результат: Anna Smirnova — результаты: 5, 4, 5; средний балл: 4.67"
    )
    assert results == results_before               # список не изменился
    assert build_report(
        student="Boris petrov",
        results=[4, 5],
        precision=1,                               # только именованные
        prefix="Итог",                             # параметры после *
    ) == "Итог: Boris Petrov — результаты: 4, 5; средний балл: 4.5"
    assert build_report("Anna", []) == "Результат: нет данных"
    assert build_report("   ", [5]) == "Результат: нет данных"

    # Проверки collect_tags
    # -----------------------------------------------------------------------
    assert collect_tags(" Python ", "python", "", " Code ") == ("python", "code")
    assert collect_tags("Python", "PYTHON", "Python", lowercase=False) == (
        "Python",
        "PYTHON",
    )
    assert collect_tags() == ()

    # Демонстрация вызовов: позиционные и именованные аргументы
    # -----------------------------------------------------------------------
    print("Позиционные и именованные аргументы:")
    print("Позиционные", arithmetic_mean([10.0, 20.0, 30.0]))
    print("Именованные", normalize_name(name="  Daria   IVANOVA "))
    print("позиционные + именованные", collect_tags("Python", "SQL", lowercase=True))

    # Демонстрация распаковки: * для списка и ** для словаря
    # -----------------------------------------------------------------------
    print("\nРаспаковка при вызове функции:")
    report_options = {"precision": 2, "prefix": "Итог"}
    report_positional_args = ["Daria IVANOVA", [3, 4, 5]]
    print(build_report(*report_positional_args, **report_options))

    # Исследование LEGB
    # -----------------------------------------------------------------------
    print() # B
    course = "Python: глобальное имя (GLOBAL)"  # G


    def outer(topic="замыкания"):
        course = f"внешняя область: {topic}"  # E

        def inner():
            nonlocal course  # L
            course = f"изменено через nonlocal (было: {course})"
            return course

        return inner


    def add_result(value, results=None):
        if results is None:
            results = []  # новый список на каждый вызов
        results.append(value)
        return results

    # Практическое расширение
    # -----------------------------------------------------------------------
    def apply_to_results(operation, values):
        return [operation(x) for x in values]

    def square(x):
        return x ** 2

    def make_threshold_checker(threshold):

        def checker(value):
            return value > threshold

        return checker

    data = [10, 25, 5, 40, 15]
    squared_data = apply_to_results(square, data)
    print(f"После square: {squared_data}")

    multiplied_data = apply_to_results(lambda x: x * 10, data)
    print(f"После lambda: {multiplied_data}")

    is_above_15 = make_threshold_checker(15)  # Первый порог
    is_above_30 = make_threshold_checker(30)  # Второй порог

    check_15 = apply_to_results(is_above_15, data)
    check_30 = apply_to_results(is_above_30, data)

    print(f"Проверка порога > 15: {check_15}")
    print(f"Проверка порога > 30: {check_30}")