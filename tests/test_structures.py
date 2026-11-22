import random
import unittest

from lab4_algorithms import Stack


class StackTests(unittest.TestCase):
    def test_empty_operations(self):
        stack = Stack()
        self.assertEqual(len(stack), 0)
        self.assertFalse(stack)
        for operation in (stack.pop, stack.peek):
            with self.assertRaises(IndexError):
                operation()
            self.assertEqual(len(stack), 0)

    def test_lifo_and_peek(self):
        stack = Stack()
        for value in [1, -2, -2, None]:
            before = len(stack)
            stack.push(value)
            self.assertEqual(len(stack), before + 1)
            self.assertEqual(stack.peek(), value)
            self.assertEqual(len(stack), before + 1)
            self.assertTrue(stack)
        self.assertEqual([stack.pop() for _ in range(4)], [None, -2, -2, 1])
        self.assertFalse(stack)
        with self.assertRaises(IndexError):
            stack.pop()
        stack.push(10)
        self.assertEqual(stack.pop(), 10)

    def test_constructor_copies_container(self):
        values = [1, 2]
        stack = Stack(values)
        values.append(3)
        self.assertEqual(len(stack), 2)
        stack.pop()
        self.assertEqual(values, [1, 2, 3])

    def test_invariants_after_mixed_operations(self):
        # Инварианты: длина равна числу оставшихся элементов,
        # bool соответствует непустоте, вершина - последний добавленный.
        rng = random.Random(24)
        stack = Stack()
        reference = []
        for _ in range(300):
            if not reference or rng.random() < 0.6:
                value = rng.randint(-20, 20)
                stack.push(value)
                reference.append(value)
            else:
                self.assertEqual(stack.pop(), reference.pop())
            self.assertEqual(len(stack), len(reference))
            self.assertEqual(bool(stack), bool(reference))
            if reference:
                self.assertEqual(stack.peek(), reference[-1])

    def test_push_pop_restores_stack(self):
        # Простой инвариант для демонстрации на защите.
        stack = Stack([10, 20])
        before = len(stack)
        stack.push(30)
        self.assertEqual(stack.pop(), 30)
        self.assertEqual(len(stack), before)
        self.assertEqual(stack.peek(), 20)
