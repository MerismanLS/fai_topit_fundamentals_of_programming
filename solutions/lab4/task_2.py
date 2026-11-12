from codecs import backslashreplace_errors

if __name__ == "__main__":

    class StepRangeIterator:
        def __init__(self, start, stop, step):
            self.start = start
            self.stop = stop
            self.step = step

        def __next__(self):
            if (self.start <= self.stop and self.step < 0) or \
               (self.stop <= self.start and self.step > 0):
                raise StopIteration
            else:
                value = self.start
                self.start += self.step
                return value


    class StepRange:
        def __init__(self, start, stop, step):
            self.start = start
            self.stop = stop
            self.step = step

        def __iter__(self):
            return StepRangeIterator(self.start, self.stop, self.step)

        def __len__(self):
            return abs(self.stop - self.start) // abs(self.step)

        def __contains__(self, value):
            between = self.start <= value <= self.stop or self.stop <= value <= self.step
            return between and abs(between - self.start) % abs(self.step) == 0

        def __repr__(self):
            return f"StepRange({self.start}, {self.stop}, {self.step})"

    r = StepRange(2, 11, 3)

    it1 = iter(r)
    it2 = iter(r)

    print("Шаг 1 (it1):", next(it1))  # 2
    print("Шаг 2 (it2):", next(it2))  # 2
    print("Шаг 3 (it1):", next(it1))  # 5
    print("Шаг 4 (it1):", next(it1))  # 8
    print("Шаг 5 (it2):", next(it2))  # 5

