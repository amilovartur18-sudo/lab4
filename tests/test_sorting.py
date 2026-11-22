import random
import unittest

from lab4_algorithms import insertion_sort, merge_sort


class SortingTests(unittest.TestCase):
    def test_required_cases(self):
        cases = [[], [5], [1, 2, 3], [3, 2, 1], [2, 2, 1, 2],
                 [-3, 0, -1, -3, 2], [7] * 30]
        for algorithm in (insertion_sort, merge_sort):
            for values in cases:
                with self.subTest(algorithm=algorithm.__name__, values=values):
                    original = values.copy()
                    result = algorithm(values)
                    self.assertEqual(result, sorted(original))
                    self.assertEqual(values, original)
                    self.assertIsNot(result, values)
                    result.append(999)
                    self.assertEqual(values, original)

    def test_random_arrays_match_reference(self):
        rng = random.Random(12345)
        for algorithm in (insertion_sort, merge_sort):
            for _ in range(100):
                values = [rng.randint(-100, 100) for _ in range(rng.randrange(150))]
                with self.subTest(algorithm=algorithm.__name__, length=len(values)):
                    original = values.copy()
                    self.assertEqual(algorithm(values), sorted(values))
                    self.assertEqual(values, original)

    def test_invalid_types(self):
        for algorithm in (insertion_sort, merge_sort):
            for values in (None, "123", (1, 2), [1, "2"], [1.5], [True]):
                with self.subTest(algorithm=algorithm.__name__, values=values):
                    with self.assertRaises(TypeError):
                        algorithm(values)

    def test_merge_on_large_basic_inputs(self):
        for values in (list(range(10000)), list(range(9999, -1, -1)), [3] * 10000):
            self.assertEqual(merge_sort(values), sorted(values))
