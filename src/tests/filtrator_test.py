import pytest
from typing import List, Dict
from filtrator import Filtrator


class TestFiltrator:
    @pytest.fixture
    def sample_data(self) -> List[Dict]:
        return [
            {"name": "Alice", "age": "30", "city": "New York", "score": "85.5"},
            {"name": "Bob", "age": "25", "city": "Los Angeles", "score": "92.0"},
            {"name": "Charlie", "age": "35", "city": "Chicago", "score": "78.3"},
            {"name": "David", "age": "30", "city": "Miami", "score": "88.9"}
        ]

    @pytest.fixture
    def filtrator(self) -> Filtrator:
        return Filtrator()

    def test_filter_condition_parser(self, filtrator):
        assert filtrator.filter_condition_parser("age>30") == ("age", ">", 30.0)
        assert filtrator.filter_condition_parser("score<90.0") == ("score", "<", 90.0)
        assert filtrator.filter_condition_parser("age=30") == ("age", "=", 30.0)
        assert filtrator.filter_condition_parser("age==30") == ("age", "==", 30.0)
        
        assert filtrator.filter_condition_parser("city=New York") == ("city", "=", "New York")
        assert filtrator.filter_condition_parser("name==Alice") == ("name", "==", "Alice")
        
        with pytest.raises(ValueError, match="неверный формат условия для фильтра"):
            filtrator.filter_condition_parser("invalid_condition")
        with pytest.raises(ValueError):
            filtrator.filter_condition_parser("age++30")
        with pytest.raises(ValueError):
            filtrator.filter_condition_parser("")

    def test_filter_data(self, filtrator, sample_data):
        assert len(filtrator.filter_data(sample_data, "age>30")) == 1
        assert len(filtrator.filter_data(sample_data, "age=30")) == 2
        assert len(filtrator.filter_data(sample_data, "score<90")) == 3
        
        assert len(filtrator.filter_data(sample_data, "city=Chicago")) == 1
        assert len(filtrator.filter_data(sample_data, "name==Bob")) == 1
        
        with pytest.raises(ValueError, match="поле 'invalid_field' не найдено в данных"):
            filtrator.filter_data(sample_data, "invalid_field>10")
            
        assert filtrator.filter_data(sample_data, "age>30")[0]["name"] == "Charlie"
        assert filtrator.filter_data(sample_data, "age<30")[0]["name"] == "Bob"
        assert {item["name"] for item in filtrator.filter_data(sample_data, "age=30")} == {"Alice", "David"}
        
        assert filtrator.filter_data(sample_data, "city=New York")[0]["name"] == "Alice"
        assert filtrator.filter_data(sample_data, "name==Bob")[0]["age"] == "25"