import math
import random
import unittest

from lab4_algorithms import gcd_iterative, gcd_recursive


class RecurrenceTests(unittest.TestCase):
    def test_known_results(self):
        for function in (gcd_iterative, gcd_recursive):
            for a, b, expected in [(48, 18, 6), (18, 48, 6), (0, 0, 0),
                                   (7, 0, 7), (0, 7, 7), (13, 17, 1), (9, 9, 9)]:
                with self.subTest(function=function.__name__, a=a, b=b):
                    self.assertEqual(function(a, b), expected)

    def test_random_inputs_match_math(self):
        rng = random.Random(98)
        for _ in range(200):
            a, b = rng.randrange(10**9), rng.randrange(10**9)
            self.assertEqual(gcd_iterative(a, b), math.gcd(a, b))
            self.assertEqual(gcd_recursive(a, b), math.gcd(a, b))

    def test_invalid_inputs(self):
        for function in (gcd_iterative, gcd_recursive):
            for a, b in [(-1, 2), (2, -1), (-1, -1)]:
                with self.assertRaises(ValueError):
                    function(a, b)
            for value in (True, 1.0, "2", None, []):
                with self.assertRaises(TypeError):
                    function(value, 2)
                with self.assertRaises(TypeError):
                    function(2, value)
