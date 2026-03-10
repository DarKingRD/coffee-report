from pathlib import Path

from coffee_report.main import format_table
from coffee_report.reports import MedianCoffeeReport, build_registry


def test_median_coffee_report_builds_sorted_result() -> None:
    records = [
        {
            "student": "Алексей Смирнов",
            "date": "2024-06-01",
            "coffee_spent": 450,
            "sleep_hours": 4.5,
            "study_hours": 12.0,
            "mood": "норм",
            "exam": "Математика",
        },
        {
            "student": "Алексей Смирнов",
            "date": "2024-06-02",
            "coffee_spent": 500,
            "sleep_hours": 4.0,
            "study_hours": 14.0,
            "mood": "устал",
            "exam": "Математика",
        },
        {
            "student": "Алексей Смирнов",
            "date": "2024-06-03",
            "coffee_spent": 550,
            "sleep_hours": 3.5,
            "study_hours": 16.0,
            "mood": "зомби",
            "exam": "Математика",
        },
        {
            "student": "Мария Соколова",
            "date": "2024-06-01",
            "coffee_spent": 100,
            "sleep_hours": 8.0,
            "study_hours": 3.0,
            "mood": "отл",
            "exam": "Математика",
        },
        {
            "student": "Мария Соколова",
            "date": "2024-06-02",
            "coffee_spent": 120,
            "sleep_hours": 8.5,
            "study_hours": 2.0,
            "mood": "отл",
            "exam": "Математика",
        },
        {
            "student": "Мария Соколова",
            "date": "2024-06-03",
            "coffee_spent": 150,
            "sleep_hours": 7.5,
            "study_hours": 4.0,
            "mood": "отл",
            "exam": "Математика",
        },
    ]

    report = MedianCoffeeReport()
    result = report.build(records)

    assert result == [
        {"student": "Алексей Смирнов", "median_coffee_spent": 500},
        {"student": "Мария Соколова", "median_coffee_spent": 120},
    ]


def test_registry_returns_report() -> None:
    registry = build_registry()
    report = registry.get("median-coffee")

    assert isinstance(report, MedianCoffeeReport)


def test_format_table_contains_headers_and_data() -> None:
    rows = [
        {"student": "Иван Кузнецов", "median_coffee_spent": 650},
        {"student": "Дарья Петрова", "median_coffee_spent": 250},
    ]

    table = format_table(rows, "median-coffee")

    assert "student" in table
    assert "median_coffee_spent" in table
    assert "Иван Кузнецов" in table
    assert "650" in table
