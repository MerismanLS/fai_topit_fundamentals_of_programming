import tracemalloc
import sys

def counter_memory(*args):
    summa = 0
    for arg in args:
        summa += sys.getsizeof(arg)
    return summa

tracemalloc.start()

empty_list = []
ten_ints_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ten_ints_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
ten_char_str = "abcdefghij"
single_int = 42
none_obj = None

current1, peak1 = tracemalloc.get_traced_memory()

tracemalloc.stop()

report1 = {
    "name": "Размеры отдельных объектов",
    "elements": 6,
    "outer_obj_size_in_bytes": counter_memory(empty_list, ten_ints_list, ten_ints_tuple, ten_char_str, single_int, none_obj),
    "current_mem_in_kb": current1 / 1024,
    "peak_mem_in_kb": peak1 / 1024
}

tracemalloc.start()

my_list = []
last_size = sys.getsizeof(my_list)

for i in range(1, 101):
    my_list.append(i)
    current_size = sys.getsizeof(my_list)

    # Выводим данные только тогда, когда размер в байтах изменился
    if current_size != last_size:
        last_size = current_size

current2, peak2 = tracemalloc.get_traced_memory()

tracemalloc.stop()

report2 = {
    "name": "Рост списка",
    "elements": 1,
    "outer_obj_size_in_bytes": counter_memory(my_list),
    "current_mem_in_kb": current2 / 1024,
    "peak_mem_in_kb": peak2 / 1024
}

tracemalloc.start()

numbers1 = list(range(100_000))

current3, peak3 = tracemalloc.get_traced_memory()

tracemalloc.stop()

tracemalloc.start()

numbers2 = range(100_000)

current4, peak4 = tracemalloc.get_traced_memory()

tracemalloc.stop()

report3 = {
    "name": "Измерение через tracemalloc 1",
    "elements": 1,
    "outer_obj_size_in_bytes": counter_memory(numbers1),
    "current_mem_in_kb": current3 / 1024,
    "peak_mem_in_kb": peak3 / 1024,
    "peak_diff": peak3 / peak4
}

report4 = {
    "name": "Измерение через tracemalloc 2",
    "elements": 1,
    "outer_obj_size_in_bytes": counter_memory(numbers2),
    "current_mem_in_kb": current4 / 1024,
    "peak_mem_in_kb": peak4 / 1024,
    "peak_diff": peak4 / peak3
}
reports = [report1, report2, report3, report4]
for report in reports:
    for key, value in report.items():
        print(f"{key}: {value}")
    print("=================")