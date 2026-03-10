"""Описание отчётов и реестра для их регистрации и получения."""
from __future__ import annotations

from abc import ABC
from collections import defaultdict
from statistics import median
from typing import Any

from coffee_report.loader import StudentRecord


class Report(ABC):
    """Базовый класс для всех отчётов."""
    name: str

    def build(self, records: list[StudentRecord]) -> list[dict[str, Any]]:
        """Строит отчёт по переданным записям."""
        raise NotImplementedError


class MedianCoffeeReport(Report):
    """Отчёт с медианой трат на кофе по студентам."""
    name = "median-coffee"

    def build(self, records: list[StudentRecord]) -> list[dict[str, Any]]:
        """Считает медиану трат на кофе для каждого студента."""
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
    """Хранилище доступных отчётов."""
    def __init__(self) -> None:
        self._reports: dict[str, Report] = {}

    def register(self, report: Report) -> None:
        """Регистрирует отчёт в реестре."""
        self._reports[report.name] = report

    def get(self, name: str) -> Report:
        """Возвращает отчёт по его имени."""
        try:
            return self._reports[name]
        except KeyError as error:
            available = ", ".join(sorted(self._reports))
            raise ValueError(
                f"Unknown report: {name}. Available reports: {available}"
            ) from error


def build_registry() -> ReportRegistry:
    """Создаёт реестр с доступными отчётами."""
    registry = ReportRegistry()
    registry.register(MedianCoffeeReport())
    return registry
