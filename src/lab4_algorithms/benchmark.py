"""Сравнение сортировок; генерация, копирование и проверка вне таймера."""

import argparse
import csv
import platform
import statistics
from pathlib import Path
from time import perf_counter

from .datasets import GENERATORS
from .sorting import insertion_sort, merge_sort

ALGORITHMS = {"insertion": insertion_sort, "merge": merge_sort}
FIELDS = ["algorithm", "dataset", "size", "repeats", "seed", "min_seconds",
          "median_seconds", "mean_seconds", "python", "platform"]


def run_benchmark(sizes=(100, 1000, 10000), repeats=5, seed=42) -> list[dict]:
    """Для каждой пары (тип, размер) фиксируется один вход.

    Каждый алгоритм получает новую копию перед каждым повтором.
    Измеряется полный вызов публичной сортировки, включая её внутреннюю
    проверку и копирование. Внешняя подготовка в измерение не входит.
    """
    if type(repeats) is not int or repeats < 5:
        raise ValueError("Нужно не менее 5 повторов")
    sizes = tuple(sizes)
    if not sizes or any(type(n) is not int or n < 0 for n in sizes):
        raise ValueError("Нужен непустой набор неотрицательных целых размеров")
    if type(seed) is not int:
        raise TypeError("Seed должен быть int (не bool)")
    rows = []
    for size in sizes:
        for dataset, generator in GENERATORS.items():
            base = generator(size, seed)
            expected = sorted(base)  # Эталон допустим вне реализации сортировок.
            for name, algorithm in ALGORITHMS.items():
                samples = []
                for _ in range(repeats):
                    values = base.copy()
                    start = perf_counter()
                    result = algorithm(values)
                    elapsed = perf_counter() - start
                    if result != expected:
                        raise RuntimeError(f"Неверная сортировка: {name}, {dataset}, {size}")
                    samples.append(elapsed)
                rows.append({
                    "algorithm": name, "dataset": dataset, "size": size,
                    "repeats": repeats, "seed": seed,
                    "min_seconds": min(samples),
                    "median_seconds": statistics.median(samples),
                    "mean_seconds": statistics.mean(samples),
                    "python": platform.python_version(), "platform": platform.platform(),
                })
    return rows


def write_csv(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", type=int, nargs="+", default=[100, 1000, 10000])
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/results.csv"))
    args = parser.parse_args()
    try:
        rows = run_benchmark(args.sizes, args.repeats, args.seed)
    except (ValueError, TypeError) as error:
        parser.error(str(error))
    write_csv(rows, args.output)
    print(f"Сохранено {len(rows)} строк: {args.output}")


if __name__ == "__main__":
    main()
