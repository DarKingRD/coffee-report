"""Загрузка и преобразование записей студентов из CSV-файлов."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import TypedDict


class StudentRecord(TypedDict):
    """Запись с данными студента за один день подготовки."""
    student: str
    date: str
    coffee_spent: int
    sleep_hours: float
    study_hours: float
    mood: str
    exam: str


def load_records(file_paths: list[str]) -> list[StudentRecord]:
    """Загружает записи студентов из CSV-файлов."""
    records: list[StudentRecord] = []

    for file_path in file_paths:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not path.is_file():
            raise FileNotFoundError(f"Not a file: {file_path}")

        with path.open(encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                records.append(
                    StudentRecord(
                        student=row["student"],
                        date=row["date"],
                        coffee_spent=int(row["coffee_spent"]),
                        sleep_hours=float(row["sleep_hours"]),
                        study_hours=float(row["study_hours"]),
                        mood=row["mood"],
                        exam=row["exam"],
                    )
                )

    return records
