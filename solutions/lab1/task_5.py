"""
Программа создаёт карточку экспериментов, где собрана вся основная информация: название эксперимента, имя исследователя, количество запуска, общее время выполнения в секундах и минутах, комплексный коэффициент и его квадрат, а также наличие выполненных запусков.
"""

person_name = input("Введите Ваше имя: ")
exp_name = input("Введите название эксперимента: ")
amount_starts = int(input("Введите количество выполненных запусков: "))
len_of_one = float(input("Введите длительность одного запуска: "))
complex_coef1 = float(input("Введите действительную часть: "))
complex_coef2 = float(input("Введите мнимую часть: "))

sum_len_sec = amount_starts * len_of_one
sum_len_min = sum_len_sec / 60
complex_coef = complex(complex_coef1, complex_coef2)
square_coef = complex_coef.real ** 2 + complex_coef.imag ** 2
has_runs = bool(amount_starts)

print("========================================")
print(f"ЭКСПЕРИМЕНТ: {exp_name}")
print(f"Исследователь: {person_name}")
print(f"Запуски: {amount_starts}")
print(f"Общее время: {sum_len_sec:.2f} с ({sum_len_min:.2f} мин)")
print(f"Коэффициент: {complex_coef}")
print(f"Квадрат модуля: {square_coef:.2f}")
print(f"Есть выполненные запуски: {has_runs}")
print("========================================")

print("========================================")
print(f"Диагностика:\nИмя: {person_name} -> {type(person_name)}\nЭксперимент: {exp_name} -> {type(exp_name)}\nСтарты: {amount_starts} -> {type(amount_starts)}\nДлительность: {len_of_one} -> {type(len_of_one)}\nДейств. часть: {complex_coef1} -> {type(complex_coef1)}\nМнимая часть: {complex_coef2} -> {type(complex_coef2)}")
print("========================================")