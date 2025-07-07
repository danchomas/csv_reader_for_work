import pytest
from typing import List, Dict
from src.aggregator import Aggregator

class TestAggregator:
    @pytest.fixture
    def sample_data(self) -> List[Dict]:
        return [
            {"name": "Alice", "age": "30", "score": "85.5"},
            {"name": "Bob", "age": "25", "score": "92.0"},
            {"name": "Charlie", "age": "35", "score": "78.3"}
        ]

    @pytest.fixture
    def aggregator(self) -> Aggregator:
        return Aggregator()

    def test_aggregate_parser(self, aggregator):
        assert aggregator.aggregate_parser("score=min") == ("score", "min")
        assert aggregator.aggregate_parser("age=max") == ("age", "max")
        assert aggregator.aggregate_parser("score=avg") == ("score", "avg")
        
        with pytest.raises(ValueError, match="неверный формат для aggregate"):
            aggregator.aggregate_parser("invalid_condition")
        with pytest.raises(ValueError):
            aggregator.aggregate_parser("score")
        with pytest.raises(ValueError):
            aggregator.aggregate_parser("")

    def test_aggregate(self, aggregator, sample_data):
        assert aggregator.aggregate(sample_data, "score=min") == [{"min": 78.3}]
        assert aggregator.aggregate(sample_data, "score=max") == [{"max": 92.0}]
        assert aggregator.aggregate(sample_data, "score=avg") == [{"avg": (85.5 + 92.0 + 78.3)/3}]
        assert aggregator.aggregate(sample_data, "age=min") == [{"min": 25.0}]
        
        with pytest.raises(KeyError, match="поле 'invalid' не найдено в данных"):
            aggregator.aggregate(sample_data, "invalid=min")
            
        with pytest.raises(ValueError, match="поле 'name' содержит нечисловые значения"):
            aggregator.aggregate(sample_data, "name=min")
            
        with pytest.raises(Exception, match="неверный оператор"):
            aggregator.aggregate(sample_data, "score=invalid")