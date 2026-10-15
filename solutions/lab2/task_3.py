import sys

data = [1, 2, 3]
print("После создания:", sys.getrefcount(data))

alias = data
print("После создания alias:", sys.getrefcount(data))

container = [data]
print("После помещения в контейнер:", sys.getrefcount(data))

del alias
print("После del alias:", sys.getrefcount(data))

container.clear()
print("После очистки контейнера:", sys.getrefcount(data))

print("====================================")

import weakref


class Record:
    pass

record = Record()
weak_record = weakref.ref(record)

print(weak_record())
del record
print(weak_record())

print("Практическое задание")

reestr = weakref.WeakValueDictionary()

r1 = Record()
r2 = Record()
wear_r3 = Record()

reestr["1"] = r1
reestr["2"] = r2
reestr["3"] = wear_r3

print("Исходный", dict(reestr))
del wear_r3
print("Удаление временной", dict(reestr))
del r1
print("Удаление сильной", dict(reestr))