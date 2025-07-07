from typing import Tuple, List, Dict

class Aggregator:
    def aggregate_parser(self, condition: str) -> Tuple[str, str]:
        try:
            field, operation = condition.split("=")
        except:
            raise ValueError("неверный формат для aggregate")
        return field, operation

    def aggregate(self, data: List[Dict], condition: str) -> str:
        field, operation = self.aggregate_parser(condition)
        if field not in data[0]:
            raise KeyError(f"поле '{field}' не найдено в данных")
        try:
            values = [float(item[field]) for item in data]
        except ValueError:
            raise ValueError(f"поле '{field}' содержит нечисловые значения")
        count = 0
        if operation == "min":
            count = min(values)
        elif operation == "max":
            count = max(values)
        elif operation == "avg":
            count = sum(values) / len(values)
        else:
            raise ValueError("неверный оператор")
        result = [{operation: count}]
        return result
