import gc
import sys

first = []
second = []

first.append(second)
second.append(first)

print("first ссылается на second:", first[0] is second)
print("second ссылается на first:", second[0] is first)

print("=== сборщик ===")
print("Состояние", gc.isenabled())
print("Поколения", gc.get_threshold())
print("Статистика", gc.get_count())
print()

first_id = id(first)
second_id = id(second)

del first
del second

deleted = gc.collect()

print("Удалено объектов:", deleted)
print()
print("Практическая задача")
node_ind = {"name": "independent", "link": []}
node_1 = {"name": "first", "link": []}
node_2 = {"name": "second", "link": []}
node_3 = {"name": "third", "link": []}

node_1["link"].append(node_2)
node_2["link"].append(node_3)
node_3["link"].append(node_1)

print("Первый ссылается на:", node_1["link"])
print("Второй ссылается на:", node_2["link"])
print("Третий ссылается на:", node_3["link"])

del node_1
del node_2
del node_3

handmade = gc.collect()
print("Удалено:", handmade)
print("Независимый объект ещё жив, его кол-во ссылок:", sys.getrefcount(node_ind))
