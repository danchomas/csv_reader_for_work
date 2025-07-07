import pytest
import csv
from typing import List, Dict
from src.reader import Reader

class TestReader:
    @pytest.fixture
    def valid_csv_file(self, tmp_path):
        file_path = tmp_path / "valid.csv"
        file_content = """name,age,city
Alice,30,New York
Bob,25,Los Angeles
Charlie,35,Chicago"""
        file_path.write_text(file_content)
        return str(file_path)

    @pytest.fixture
    def empty_csv_file(self, tmp_path):
        file_path = tmp_path / "empty.csv"
        file_content = "name,age,city"
        file_path.write_text(file_content)
        return str(file_path)

    def test_init_and_get_data(self, valid_csv_file, empty_csv_file):
        reader = Reader(valid_csv_file)
        data = reader.get_data()
        
        assert isinstance(data, list)
        assert len(data) == 3
        assert data == [
            {"name": "Alice", "age": "30", "city": "New York"},
            {"name": "Bob", "age": "25", "city": "Los Angeles"},
            {"name": "Charlie", "age": "35", "city": "Chicago"}
        ]
        
        assert all(isinstance(row, dict) for row in data)
        
        with pytest.raises(Exception, match="файл пуст"):
            Reader(empty_csv_file)
            
        with pytest.raises(Exception, match="файл не был найден"):
            Reader("non_existent_file.csv")
