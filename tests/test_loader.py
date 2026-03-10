from pathlib import Path

import pytest

from coffee_report.loader import load_records


def test_load_records_from_multiple_files(tmp_path: Path) -> None:
    """Проверяет загрузку записей из нескольких файлов."""
    first = tmp_path / "part1.csv"
    second = tmp_path / "part2.csv"

    first.write_text(
        (
            "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
            "Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика\n"
        ),
        encoding="utf-8",
    )
    second.write_text(
        (
            "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
            "Дарья Петрова,2024-06-01,200,7.0,6,отл,Математика\n"
        ),
        encoding="utf-8",
    )

    records = load_records([str(first), str(second)])

    assert len(records) == 2
    assert records[0]["student"] == "Алексей Смирнов"
    assert records[0]["coffee_spent"] == 450
    assert records[1]["student"] == "Дарья Петрова"
    assert records[1]["coffee_spent"] == 200


def test_load_records_raises_for_missing_file() -> None:
    """Проверяет ошибку при отсутствии файла."""
    with pytest.raises(FileNotFoundError, match="File not found"):
        load_records(["missing.csv"])
