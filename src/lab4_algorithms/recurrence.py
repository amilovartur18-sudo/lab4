"""Итеративный и рекурсивный алгоритм Евклида."""


def _validate(a: int, b: int) -> None:
    if type(a) is not int or type(b) is not int:
        raise TypeError("Аргументы должны быть целыми числами (не bool)")
    if a < 0 or b < 0:
        raise ValueError("Аргументы должны быть неотрицательными")


def gcd_iterative(a: int, b: int) -> int:
    """НОД неотрицательных int; НОД(0, 0) = 0.

    Неверный тип вызывает TypeError, отрицательное число - ValueError.
    """
    _validate(a, b)
    while b != 0:
        a, b = b, a % b
    return a


def gcd_recursive(a: int, b: int) -> int:
    """НОД с тем же контрактом; глубина ограничена стеком Python.

    При слишком глубокой рекурсии возможен RecursionError.
    """
    _validate(a, b)
    return _gcd_recursive(a, b)


def _gcd_recursive(a: int, b: int) -> int:
    if b == 0:
        return a
    return _gcd_recursive(b, a % b)
