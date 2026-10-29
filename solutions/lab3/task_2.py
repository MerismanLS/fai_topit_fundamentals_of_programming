measurements = [12, 15, 11, 18, 18, 9, 21, 15, 7, 18]

summa = 0
minim = float('inf')
maxim = float('-inf')
even_count = 0

for el in measurements:
    summa += el

    if el > maxim:
        maxim = el

    if el < minim:
        minim = el

    if el % 2 == 0:
        even_count += 1

avg = summa / len(measurements)
count_more_avg = 0

for el in measurements:
    if el > avg:
        count_more_avg += 1

print("Сумма:", summa)
print("Минимальный элемент:", minim)
print("Максимальный элемент:", maxim)
print("Кол-во чётных чисел:", even_count)
print("Кол-во чисел больше среднего арифметического:", count_more_avg)

def linear_search(arr, x):
    result = -1
    comparisons = 0
    for i in range(len(arr)):
        if arr[i] == x:
            result = i
        comparisons += 1
    return result, comparisons

def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            comparisons += 1
            return mid, comparisons
        elif x < arr[mid]:
            comparisons += 1
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons

def prime(n):
    if n == 1: return True
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def selection_sort(arr):
    for i in range(len(arr)-1):
        min_idx = i

        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j

        if i != min_idx:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

import random

unsorted_10 = [random.randint(1, 10) for i in range(10)]
sorted_10 = selection_sort(unsorted_10)

unsorted_100 = [random.randint(1, 100) for i in range(100)]
sorted_100 = selection_sort(unsorted_100)

unsorted_1000 = [random.randint(1, 1000) for i in range(1000)]
sorted_1000 = selection_sort(unsorted_1000)

print(linear_search(sorted_10, random.randint(1, 10)))
print(linear_search(sorted_100, random.randint(1, 100)))
print(linear_search(sorted_1000, random.randint(1, 1000)))

print(binary_search(sorted_10, random.randint(1, 10)))
print(binary_search(sorted_100, random.randint(1, 100)))
print(binary_search(sorted_1000, random.randint(1, 1000)))