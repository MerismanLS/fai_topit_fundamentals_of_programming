print("эксперимент А")
x = 17
y = 5

print("x + y =", x + y, type(x + y))
print("x - y =", x - y, type(x - y))
print("x * y =", x * y, type(x * y))
print("x / y =", x / y, type(x / y))
print("x // y =", x // y, type(x // y))
print("x % y =", x % y, type(x % y))
print("x ** y =", x ** y, type(x ** y))
print()

print("эксперимент B")

print("2 ** 1000:", 2 ** 1000)
print()

print("эксперимент C")
import math

result = 0.1 + 0.2

print("result:", result)
print("result == 0.3:", result == 0.3)
print("result - 0.4:", result - 0.4)
print("проверка math.isclose:", math.isclose(result, 0.3))
print()

print("Эксперимент D")

str_to_int = int("42")
str_to_float = float("3.14")
int_to_str = str(2026)
int_to_bool = bool(0)
nint_to_bool = bool(-1)
empty_str_to_bool = bool("")
str_to_bool = bool("False")
my_complex = complex(2, -3)

print("строка в целое число:", str_to_int, type(str_to_int))
print("строка в вещ. число:", str_to_float, type(str_to_float))
print("целое число в строку:", int_to_str, type(int_to_str))
print("целое число в булево значение:", int_to_bool, type(int_to_bool))
print("отрицательное целое число в булево значение:", nint_to_bool, type(nint_to_bool))
print("пустая строка в булево значение:", empty_str_to_bool, type(empty_str_to_bool))
print("строка в булево значение:", str_to_bool, type(str_to_bool))
print("комплексное число:", my_complex, type(my_complex))
my2_complex = complex(2, 3)
print("Действительная и мнимая части комплексного числа:", my2_complex.real, my2_complex.imag)
