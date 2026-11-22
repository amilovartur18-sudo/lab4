"""Сортировки возвращают новый список и не меняют исходный."""


def _copy_input(values: list[int]) -> list[int]:
    if not isinstance(values, list):
        raise TypeError("Ожидается список целых чисел")
    if any(type(value) is not int for value in values):
        raise TypeError("Все элементы должны быть int (не bool)")
    return values.copy()


def insertion_sort(values: list[int]) -> list[int]:
    """Новый отсортированный список int. Неверный тип: TypeError.

    Время O(n²), на отсортированном входе O(n); память O(n) для копии.
    """
    result = _copy_input(values)
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and result[j] > current:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def merge_sort(values: list[int]) -> list[int]:
    """Новый отсортированный список int. Неверный тип: TypeError.

    Время O(n log n), пиковая дополнительная память O(n).
    """
    return _merge_sort(_copy_input(values))


def _merge_sort(values: list[int]) -> list[int]:
    if len(values) < 2:
        return values
    middle = len(values) // 2
    left = _merge_sort(values[:middle])
    right = _merge_sort(values[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
