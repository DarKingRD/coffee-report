"""Точка входа CLI для построения отчётов по CSV-файлам."""
from __future__ import annotations

import argparse
import sys

from tabulate import tabulate

from coffee_report.loader import load_records
from coffee_report.reports import build_registry


def parse_args() -> argparse.Namespace:
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Build reports from students exam preparation CSV files."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths to CSV files.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Report name to build.",
    )
    return parser.parse_args()


def format_table(rows: list[dict[str, object]], report_name: str) -> str:
    """Форматирует строки отчёта в виде таблицы."""
    if report_name == "median-coffee":
        headers = {
            "student": "student",
            "median_coffee_spent": "median_coffee_spent",
        }
        return tabulate(rows, headers=headers, tablefmt="github")

    raise ValueError(f"Unsupported report formatting: {report_name}")


def run() -> int:
    """Запускает построение отчёта и выводит его в консоль."""
    args = parse_args()

    try:
        records = load_records(args.files)
        registry = build_registry()
        report = registry.get(args.report)
        rows = report.build(records)
        print(format_table(rows, args.report))
    except (FileNotFoundError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(run())
