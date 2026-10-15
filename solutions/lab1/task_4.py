student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10
percent = 7/10

print("Первый символ:", student[0])
print("Последний символ:", student[3])
print("Срез с именем:", student[0:student.find(" "):])
print("Срез с фамилией:", student[student.find(" ") + 1::])
print("Верхний регистр:", student.lower())
print("Нижний регистр:", student.upper())
print("Инициалы: ", student[0], ".", student[student.find(" ") +1], ".", sep="")
print("В обратном порядке:", course[0:0:-1])
print("Способ %:", "%s - %s: %d/%d (%.1f%%)" % (student, course, completed, total, percent * 100))
print("Способ .format:", "{} - {}: {}/{} ({:.1%})".format(student, course, completed, total, percent))
print("Способ f-строка:", f"{student} - {course}: {completed}/{total} ({percent:.1%})")
print()
symbol = "Я"
print("Вывод символа:", symbol)
print("Использование функции ord():", ord(symbol))
print("Вывод chr(ord(symbol)):", chr(ord(symbol)))
print("Код символа:", symbol.encode("utf-8"))
print("Длина кода символа:", len(symbol.encode("utf-8")))

symbol[0] = "a"
print(symbol)