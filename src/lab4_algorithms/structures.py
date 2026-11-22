"""Стек: последним добавлен - первым извлечён (LIFO)."""

from collections.abc import Iterable
from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """Стек произвольных объектов; pop/peek пустого стека дают IndexError."""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._items = list(values)

    def push(self, value: T) -> None:
        """Добавить значение на вершину."""
        self._items.append(value)

    def pop(self) -> T:
        """Извлечь вершину; IndexError, если стек пуст."""
        if not self._items:
            raise IndexError("Стек пуст")
        return self._items.pop()

    def peek(self) -> T:
        """Прочитать вершину без удаления; IndexError, если стек пуст."""
        if not self._items:
            raise IndexError("Стек пуст")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)
