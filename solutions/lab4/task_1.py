if __name__ == "__main__":
    values = [10, 20, 30]
    iterator = iter(values)

    print(iterator is values)
    print(iter(iterator) is iterator)
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))



    def consume(iterable) -> list:
        result = []
        iterable = iter(iterable)
        try:
            while iterable:
                result.append(next(iterable))
        except StopIteration:
            return result


    # практическое расширение
    def my_enumerate(iterable, start=0):
        idx = start
        for elem in iterable:
            yield idx, elem
            idx += 1

    def my_zip(first, second):
        first = iter(first)
        second = iter(second)
        while True:
            try:
                yield next(first), next(second)
            except StopIteration:
                break