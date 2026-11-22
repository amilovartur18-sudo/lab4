"""Пять типов входа; случайность изолирована в random.Random(seed)."""

import random


def _validate(size: int, seed: int | None) -> None:
    if type(size) is not int:
        raise TypeError("Размер должен быть int (не bool)")
    if size < 0:
        raise ValueError("Размер не может быть отрицательным")
    if seed is not None and type(seed) is not int:
        raise TypeError("Seed должен быть int или None")


def random_data(size: int, seed: int | None = None) -> list[int]:
    """size случайных целых из [-size, size]."""
    _validate(size, seed)
    rng = random.Random(seed)
    return [rng.randint(-size, size) for _ in range(size)]


def sorted_data(size: int, seed: int | None = None) -> list[int]:
    """Случайный набор по возрастанию; seed определяет значения."""
    # Встроенная сортировка допустима при подготовке тестовых данных.
    return sorted(random_data(size, seed))


def reversed_data(size: int, seed: int | None = None) -> list[int]:
    """Тот же случайный набор по убыванию."""
    return list(reversed(sorted_data(size, seed)))


def nearly_sorted_data(size: int, seed: int | None = None) -> list[int]:
    """Возрастающий набор после max(1, size // 100) случайных обменов.

    При size < 2 обменов нет. Каждый обмен выбирает разные позиции.
    """
    result = sorted_data(size, seed)
    rng = random.Random(seed)
    if size >= 2:
        for _ in range(max(1, size // 100)):
            first, second = rng.sample(range(size), 2)
            result[first], result[second] = result[second], result[first]
    return result


def duplicates_data(size: int, seed: int | None = None) -> list[int]:
    """Случайные целые из пяти значений: -2, -1, 0, 1, 2."""
    _validate(size, seed)
    rng = random.Random(seed)
    return [rng.randint(-2, 2) for _ in range(size)]


GENERATORS = {
    "random": random_data,
    "sorted": sorted_data,
    "reversed": reversed_data,
    "nearly_sorted": nearly_sorted_data,
    "duplicates": duplicates_data,
}
