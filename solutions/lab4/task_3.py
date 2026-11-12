from collections import deque

if __name__ == "__main__":
    def read_measurenets(lines):
        for line in lines:
            if line.strip() == "":
                continue
            yield float(line.strip())

    def filter_range(values, minimum:float, maximum:float):
        for value in values:
            if minimum <= value <= maximum:
                yield value

    def moving_average(values, window_size: int):
        if window_size <= 0: raise ValueError("window_size must be > 0")

        # окном является дека
        window = deque(maxlen=window_size)
        current_sum = 0.0

        for value in values:
            if len(window) == window_size:
                current_sum -= window[0]
            window.append(value)
            current_sum += value

            if len(window) == window_size:
                yield current_sum / window_size

    def conveyer(values, minimum, maximum, window_size):
        first = read_measurenets(values)
        second = filter_range(first, minimum, maximum)
        return moving_average(second, window_size)


    raw_lines = [f"{x % 41 * 0.75}" for x in range(10000)]

    for el in conveyer(raw_lines, 11, 50, 2):
        print(el)

    # дополнительно
    even_squares = [x**2 for x in range(1, 21) if x ** 2 == 0]
    strings = [len(line) for line in raw_lines if line.strip()]
    tens = {x: x**2 for x in range(1, 11)}
    summa = sum(x**2 for x in range(1, 1000))

    # практическое расширение
    def take(n: int, iterable):
        # выдаёт первые n элементов
        if n <= 0:
            return
        for index, item in enumerate(iterable):
            yield item
            if index + 1 >= n:
                break


    def drop(n: int, iterable):
        # пропускает первые n элементов
        iterator = iter(iterable)
        for _ in range(n):
            try:
                next(iterator)
            except StopIteration:
                return
        yield from iterator

    def batch(iterable, size: int):
        if size <= 0:
            raise ValueError("Размер пакета должен быть положительным")
        chunk = []
        for item in iterable:
            chunk.append(item)
            if len(chunk) == size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    import tracemalloc

    def conveyer2(values, minimum, maximum, window_size):
        nums = [float(line.strip()) for line in values if line.strip()]
        filtered = [x for x in nums if minimum <= x <= maximum]
        averages = [
            sum(filtered[i - window_size + 1: i + 1]) / window_size
            for i in range(window_size - 1, len(filtered))
        ]
        return averages


    def lazy_con():
        tracemalloc.start()
        source = (f"{x % 41 * 0.75}" for x in range(10000))
        pipe_stream = conveyer(source, 5, 25, 5)
        batches = batch(take(50_000, drop(100, pipe_stream)), 100)
        for _ in batches:
            pass
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak


    def list_con():
        tracemalloc.start()
        source = [f"{x % 41 * 0.75}" for x in range(10000)]
        nums = [float(line.strip()) for line in source if line.strip()]
        filtered = [x for x in nums if 5 <= x <= 25]
        w = 5
        averages = [
            sum(filtered[i - w + 1: i + 1]) / w
            for i in range(w - 1, len(filtered))
        ]
        sliced = averages[100: 100 + 50_000]
        batches = [sliced[i: i + 100] for i in range(0, len(sliced), 100)]
        for _ in batches:
            pass
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak

    lazy_peak = lazy_con()
    list_peak = list_con()

    print(f"Пиковая память (ленивый конвейер): {lazy_peak / 1024:.2f} КБ")
    print(f"Пиковая память (со списками):      {list_peak / 1024:.2f} КБ")