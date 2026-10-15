a = 1000
b = a
a = int('1000')
c = None

print("Переменная a:", "тип:", type(a), "идентификатор:", id(a))
print("Переменная b:", "тип:", type(b), "идентификатор:", id(b))
print("Переменная c:", "тип:", type(c), "идентификатор:", id(c))
print("a == b:", a == b)
print("a is b:", a is b)
print("a == c:", a == c)
print("a is c:", a is c)
print("c == None", c == None)
print("c is None", c is None)

first = "python"
second = "py" + "thon"

print("first == second:", first == second)
print("first is second:", first is second)