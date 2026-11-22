import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from lab4_algorithms import benchmark


class BenchmarkTests(unittest.TestCase):
    def test_methodology_without_real_clock(self):
        events, inputs = [], []

        class TrackedList(list):
            def copy(self):
                events.append("copy")
                return super().copy()

        def generator(size, seed):
            events.append("generate")
            self.assertEqual((size, seed), (3, 42))
            return TrackedList([3, 1, 2])

        def sorter(values):
            events.append("sort")
            inputs.append(values)  # Сохраняем ссылки для проверки независимости.
            self.assertEqual(values, [3, 1, 2])
            result = sorted(values)
            values.clear()  # Даже мутирующий алгоритм не портит следующий запуск.
            return result

        ticks = iter(range(20))

        def clock():
            events.append("clock")
            return next(ticks)

        with patch.dict(benchmark.GENERATORS, {"test": generator}, clear=True), \
             patch.dict(benchmark.ALGORITHMS, {"a": sorter, "b": sorter}, clear=True), \
             patch.object(benchmark, "perf_counter", clock):
            rows = benchmark.run_benchmark([3], 5, 42)
        self.assertEqual(events, ["generate"] + ["copy", "clock", "sort", "clock"] * 10)
        self.assertEqual(len({id(values) for values in inputs}), 10)
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(row["median_seconds"], 1)
            self.assertEqual(row["mean_seconds"], 1)
            self.assertEqual(row["min_seconds"], 1)
            self.assertEqual(row["repeats"], 5)

    def test_all_combinations_and_csv(self):
        with patch.object(benchmark, "perf_counter", side_effect=range(400)):
            rows = benchmark.run_benchmark([0, 1, 10], 5)
        self.assertEqual(len(rows), 30)
        self.assertEqual({row["dataset"] for row in rows}, set(benchmark.GENERATORS))
        self.assertEqual({row["algorithm"] for row in rows}, {"insertion", "merge"})
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "nested" / "results.csv"
            benchmark.write_csv(rows, output)
            with output.open(encoding="utf-8", newline="") as stream:
                reader = csv.DictReader(stream)
                self.assertEqual(reader.fieldnames, benchmark.FIELDS)
                saved = list(reader)
            self.assertEqual(len(saved), 30)
            self.assertTrue(all(row["repeats"] == "5" for row in saved))

    def test_incorrect_sort_is_rejected(self):
        with patch.dict(benchmark.ALGORITHMS, {"broken": lambda values: []}, clear=True), \
             patch.object(benchmark, "perf_counter", side_effect=[0, 1]):
            with self.assertRaises(RuntimeError):
                benchmark.run_benchmark([3])

    def test_invalid_arguments(self):
        for repeats in (0, 4, 5.0, True):
            with self.assertRaises(ValueError):
                benchmark.run_benchmark([1], repeats)
        for sizes in ([], [-1], [True], [1.5]):
            with self.assertRaises(ValueError):
                benchmark.run_benchmark(sizes)
        with self.assertRaises(TypeError):
            benchmark.run_benchmark([1], seed="42")
