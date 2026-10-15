print("Эксперимент A")

a = 10
b = a

print(a, b)
print(id(a), id(b))

a += 1

print(a, b)
print(id(a), id(b))

print()
print("Эксперимент B")
first = [10, 20]
second = first

print(first, second)
print(id(first), id(second))

second.append(30)

print(first, second)
print(id(first), id(second))

print()
print("Дополнение")

second = [10, 20, 30]

print(first, second)
print(first == second)
print(first is second)

second.append(40)
first.append(40)

print(first, second)
print(first == second)
print(first is second)

print()
print("Практическое задание")

config1 = {
    "name": "project_test",
    "users": ["Sergo", "Nikita", "Kostya"],
    "params": [True, 69, False, 67]
}

config2 = config1
print("===== Некорректное копирование =====")
print("До изменений в первой конфигурации")
print(config1["name"], config2["name"])
config1["name"] = "not_test"
print("После изменений в первой конфигурации")
print(config1["name"], config2["name"])

config3 = config1.copy()
print("===== Правильное копирование =====")
print("До изменений в первой конфигурации")
print(config1["name"], config3["name"])
config1["name"] = "tochno_ne_test"
config1["users"] = ["Nobody", "Toxis"]
print("После изменений в первой конфигурации")
print(config1["name"], config3["name"])

assert config1 is not config3, "Всё-таки одинаковые"
assert config1["users"] is not config3["users"], "Всё-таки одинаковые"
assert config1["params"] is not config3["params"], "Всё-таки одинаковые"