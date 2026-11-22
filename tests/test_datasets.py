import random
import unittest

from lab4_algorithms.datasets import (GENERATORS, random_data, sorted_data,
                                     reversed_data, nearly_sorted_data, duplicates_data)


class DatasetTests(unittest.TestCase):
    def test_size_type_and_reproducibility(self):
        for name, generator in GENERATORS.items():
            for size in (0, 1, 100):
                with self.subTest(generator=name, size=size):
                    first = generator(size, 42)
                    second = generator(size, 42)
                    self.assertEqual(first, second)
                    self.assertIsNot(first, second)
                    self.assertEqual(len(first), size)
                    self.assertTrue(all(type(x) is int for x in first))

    def test_different_seeds_for_randomized_generators(self):
        for generator in GENERATORS.values():
            self.assertNotEqual(generator(1000, 42), generator(1000, 43))

    def test_shapes(self):
        expected = sorted(random_data(100, 42))
        self.assertEqual(sorted_data(100, 42), expected)
        self.assertEqual(reversed_data(100, 42), expected[::-1])
        self.assertTrue(all(-100 <= x <= 100 for x in random_data(100, 42)))
        values = duplicates_data(100, 42)
        self.assertTrue(set(values) <= {-2, -1, 0, 1, 2})
        self.assertLess(len(set(values)), len(values))
        for size in (0, 1, 2, 100, 1000):
            original = sorted_data(size, 42)
            nearly = nearly_sorted_data(size, 42)
            self.assertEqual(sorted(nearly), original)
            changed = sum(a != b for a, b in zip(nearly, original))
            self.assertLessEqual(changed, 2 * max(1, size // 100))

    def test_global_random_state_is_unchanged(self):
        before = random.getstate()
        for generator in GENERATORS.values():
            generator(100, 42)
            generator(100)
        self.assertEqual(random.getstate(), before)

    def test_output_does_not_depend_on_global_random_state(self):
        before = random.getstate()
        try:
            for generator in GENERATORS.values():
                random.seed(1)
                first = generator(100, 42)
                random.seed(999)
                self.assertEqual(generator(100, 42), first)
        finally:
            random.setstate(before)

    def test_invalid_inputs(self):
        for generator in GENERATORS.values():
            with self.assertRaises(ValueError):
                generator(-1)
            for size in (True, 1.0, "2", None):
                with self.assertRaises(TypeError):
                    generator(size)
            for seed in (True, 1.5, "42"):
                with self.assertRaises(TypeError):
                    generator(10, seed)
