"""Тесты для расчёта отчётов, форматирования таблицы и сценариев CLI."""
from pathlib import Path

from coffee_report.main import format_table, run
from coffee_report.reports import MedianCoffeeReport, build_registry


SAMPLE_CSV = """student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика
Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика
Мария Соколова,2024-06-01,100,8.0,3,отл,Математика
Мария Соколова,2024-06-02,120,8.5,2,отл,Математика
"""


def test_median_coffee_report_builds_sorted_result() -> None:
    """Проверяет расчёт и сортировку медианных трат на кофе."""
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
    """Проверяет получение отчёта из реестра по имени."""
    registry = build_registry()
    report = registry.get("median-coffee")

    assert isinstance(report, MedianCoffeeReport)


def test_registry_raises_error_for_unknown_report() -> None:
    """Проверяет ошибку при запросе неизвестного отчёта."""
    registry = build_registry()

    try:
        registry.get("unknown-report")
    except ValueError as error:
        assert "Unknown report: unknown-report" in str(error)
    else:
        raise AssertionError("ValueError was not raised")


def test_format_table_contains_friendly_headers_and_data() -> None:
    """Проверяет форматирование отчёта в таблицу с понятными заголовками."""
    rows = [
        {"student": "Иван Кузнецов", "median_coffee_spent": 650},
        {"student": "Дарья Петрова", "median_coffee_spent": 250},
    ]

    table = format_table(rows, "median-coffee")

    assert "student" in table
    assert "median_coffee_spent" in table
    assert "Иван Кузнецов" in table
    assert "650" in table


def test_run_returns_error_for_unknown_report(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    """Проверяет, что run возвращает код 1 для неизвестного отчёта."""
    file_path = tmp_path / "data.csv"
    file_path.write_text(SAMPLE_CSV, encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "coffee_report",
            "--files",
            str(file_path),
            "--report",
            "unknown-report",
        ],
    )

    exit_code = run()
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert "Unknown report: unknown-report" in captured.err


def test_run_prints_report_for_valid_arguments(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    """Проверяет успешное построение и вывод отчёта в консоль."""
    file_path = tmp_path / "data.csv"
    file_path.write_text(SAMPLE_CSV, encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "coffee_report",
            "--files",
            str(file_path),
            "--report",
            "median-coffee",
        ],
    )

    exit_code = run()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.err == ""
    assert "student" in captured.out
    assert "median_coffee_spent" in captured.out
    assert "Алексей Смирнов" in captured.out
