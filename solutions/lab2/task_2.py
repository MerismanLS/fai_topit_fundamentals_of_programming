import copy

original = [
    ["Python", 5],
    ["Algorithms", 4],
]

alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

original.append(["Databases", 5])
original[0][1] = 3

print("original:", original)
print("alias:", alias)
print("shallow:", shallow)
print("deep:", deep)
print()
print("id original:", id(original))
print("id alias:", id(alias))
print("id shallow:", id(shallow))
print("id deep:", id(deep))
print()
print("id[0] original:", id(original[0]))
print("id[0] alias:", id(alias[0]))
print("id[0] shallow:", id(shallow[0]))
print("id[0] deep:", id(deep[0]))
print()
print("id[0][1] original:", id(original[0][1]))
print("id[0][1] alias:", id(alias[0][1]))
print("id[0][1] shallow:", id(shallow[0][1]))
print("id[0][1] deep:", id(deep[0][1]))
print("=================================")
wrong_matrix = [[0] * 3] * 3
wrong_matrix[0][0] = 1
print(wrong_matrix)
print()
correct_matrix = [[0] * 3 for _ in range(3)]
correct_matrix[0][0] = 1
print(correct_matrix)