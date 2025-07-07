import pytest
import csv
from typing import List, Dict
from reader import Reader

class TestReader:
    @pytest.fixture
    def valid_csv_file(self, tmp_path):
        """Фикстура с валидным CSV файлом."""
        file_path = tmp_path / "valid.csv"
        file_content = """name,age,city
Alice,30,New York
Bob,25,Los Angeles
Charlie,35,Chicago"""
        file_path.write_text(file_content)
        return str(file_path)

    @pytest.fixture
    def empty_csv_file(self, tmp_path):
        """Фикстура с пустым CSV файлом (только заголовки)."""
        file_path = tmp_path / "empty.csv"
        file_content = "name,age,city"  # Только заголовки
        file_path.write_text(file_content)
        return str(file_path)

    @pytest.fixture
    def invalid_csv_file(self, tmp_path):
        """Фикстура с битым CSV файлом (неправильный формат)."""
        file_path = tmp_path / "invalid.csv"
        file_content = "name,age,city\nAlice,30"
        file_path.write_text(file_content)
        return str(file_path)

    def test_read_valid_file(self, valid_csv_file):
        """Тест чтения валидного CSV файла."""
        reader = Reader(valid_csv_file)
        data = reader.get_data()

        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0] == {"name": "Alice", "age": "30", "city": "New York"}
        assert data[1] == {"name": "Bob", "age": "25", "city": "Los Angeles"}
        assert data[2] == {"name": "Charlie", "age": "35", "city": "Chicago"}

    def test_read_empty_file(self, empty_csv_file):
        """Тест обработки пустого CSV файла (только заголовки)."""
        with pytest.raises(Exception) as exc_info:
            Reader(empty_csv_file)
        assert str(exc_info.value) == "файл пуст"

    def test_read_nonexistent_file(self):
        """Тест обработки несуществующего файла."""
        with pytest.raises(Exception) as exc_info:
            Reader("non_existent_file.csv")
        assert str(exc_info.value) == "файл не был найден"

    def test_get_data_returns_list_of_dicts(self, valid_csv_file):
        """Тест, что get_data() возвращает список словарей."""
        reader = Reader(valid_csv_file)
        data = reader.get_data()
        assert isinstance(data, list)
        assert all(isinstance(row, dict) for row in data)

