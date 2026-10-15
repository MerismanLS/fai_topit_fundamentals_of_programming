import sys

empty_list = []
ten_ints_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ten_ints_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
ten_char_str = "abcdefghij"
single_int = 42
none_obj = None

print(f"Пустой список: {sys.getsizeof(empty_list)} байт")
print(f"Список из 10 чисел: {sys.getsizeof(ten_ints_list)} байт")
print(f"Кортеж из 10 чисел: {sys.getsizeof(ten_ints_tuple)} байт")
print(f"Строка из 10 символов: {sys.getsizeof(ten_char_str)} байт")
print(f"Целое число: {sys.getsizeof(single_int)} байт")
print(f"Объект None: {sys.getsizeof(none_obj)} байт")

print("================================")

my_list = []
last_size = sys.getsizeof(my_list)

print(f"Начальное состояние: Длина = {len(my_list)}, Размер = {last_size} байт\n")

for i in range(1, 101):
    my_list.append(i)
    current_size = sys.getsizeof(my_list)

    # Выводим данные только тогда, когда размер в байтах изменился
    if current_size != last_size:
        print(f"Длина = {len(my_list)}, Размер = {current_size} байт (изменился при добавлении {i}-го элемента)")
        last_size = current_size

print("================================")

import tracemalloc


tracemalloc.start()

list_range = list(range(100_000))

current, peak = tracemalloc.get_traced_memory()

tracemalloc.stop()

print(f"Текущая память: {current / 1024:.2f} КБ")
print(f"Пиковая память: {peak / 1024:.2f} КБ\n")


tracemalloc.start()

just_range = range(100_000)

current, peak = tracemalloc.get_traced_memory()

tracemalloc.stop()

print(f"Текущая память: {current / 1024:.2f} КБ")
print(f"Пиковая память: {peak / 1024:.2f} КБ\n")

