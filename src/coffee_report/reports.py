from __future__ import annotations

from abc import ABC
from collections import defaultdict
from statistics import median
from typing import Any

from coffee_report.loader import StudentRecord


class Report(ABC):
    name: str

    def build(self, records: list[StudentRecord]) -> list[dict[str, Any]]:
        raise NotImplementedError


class MedianCoffeeReport(Report):
    name = "median-coffee"

    def build(self, records: list[StudentRecord]) -> list[dict[str, Any]]:
        spent_by_student: dict[str, list[int]] = defaultdict(list)

        for record in records:
            spent_by_student[record["student"]].append(record["coffee_spent"])

        result = [
            {
                "student": student,
                "median_coffee_spent": median(spent_values),
            }
            for student, spent_values in spent_by_student.items()
        ]

        result.sort(key=lambda row: row["median_coffee_spent"], reverse=True)
        return result


class ReportRegistry:
    def __init__(self) -> None:
        self._reports: dict[str, Report] = {}

    def register(self, report: Report) -> None:
        self._reports[report.name] = report

    def get(self, name: str) -> Report:
        try:
            return self._reports[name]
        except KeyError as error:
            available = ", ".join(sorted(self._reports))
            raise ValueError(
                f"Unknown report: {name}. Available reports: {available}"
            ) from error


def build_registry() -> ReportRegistry:
    registry = ReportRegistry()
    registry.register(MedianCoffeeReport())
    return registry
