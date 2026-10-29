submissions = [
    ("anna", "lab_01", 5),
    ("boris", "lab_01", 4),
    ("anna", "lab_02", 5),
    ("daria", "lab_01", 3),
    ("boris", "lab_02", 5),
    ("anna", "lab_01", 4),
]
# 1
students = set(el[0] for el in submissions)

# 2
labs = set(el[1] for el in submissions)

# 3
stud_tries = {}
for el in submissions:
    stud_tries.setdefault(el[0], []).append(el[2])

# 4
best_tries = {}
for el in submissions:
    key = (el[0], el[1])
    if key not in best_tries or best_tries[key] < el[2]:
        best_tries[key] = el[2]

# 5
attempts = {}
for el in submissions:
    key = (el[0], el[1])
    attempts[key] = attempts.get(key, 0) + 1

# extra
stud_labs = {}
for el in submissions:
    stud_labs.setdefault(el[1], set()).add(el[0])

print(stud_labs['lab_01'] & stud_labs['lab_02'])

# adding
new_student = ("oleg", "lab_01", 4)

# 0
submissions.append(new_student)

# 1
students.add(new_student[0])

# 2
labs.add(new_student[1])

# 3
stud_tries.setdefault(new_student[0], []).append(new_student[2])

# 4
key = (new_student[0], new_student[1])
if key not in best_tries or best_tries[key] < new_student[2]:
    best_tries[key] = new_student[2]

# 5
key = (new_student[0], new_student[1])
attempts[key] = attempts.get(key, 0) + 1

# расширение

stud_all_labs = {}
for el in submissions:
    stud_all_labs.setdefault(el[0], set()).add(el[1])

while True:
    try:
        command = input("Ввелите команду: ").split()
        if command[0] == "student":
            print("Список всех сданных лабораторных:", *stud_all_labs[command[1]])
        if command[0] == "best":
            print(f"Лучшая попытка сдачи {command[2]}:", best_tries[(command[1], command[2])])
        if command[0] == "attempts":
            print(f"Количество попыток для сдачи {command[2]}:", attempts[(command[1], command[2])])
        if command[0] == "completed":
            print(f"Студенты, выполнившие {command[1]}:", *stud_labs[command[1]])
    except Exception as e:
        print("Вы оплошались в наборе команды, попробуйте снова")