import pytest
from src.presenter import Presenter

class TestPresenter:
    def test_print_data(self):
        normal_data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Los Angeles"}
        ]
        normal_result = Presenter.print_data(normal_data)
        assert isinstance(normal_result, str)
        assert all(x in normal_result for x in ["Alice", "30", "New York", "Bob", "25", "Los Angeles"])
        
        empty_result = Presenter.print_data([])
        assert isinstance(empty_result, str)
        
        malformed_data = [{"name": "Alice"}, {"age": 25}]
        malformed_result = Presenter.print_data(malformed_data)
        assert isinstance(malformed_result, str)
        assert "Alice" in malformed_result and "25" in malformed_result
        
        assert "+------" in normal_result
        assert "| name " in normal_result 