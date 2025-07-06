import csv
import argparse
import re
import sys
from typing import List, Dict, Tuple, Union
from tabulate import tabulate


class Reader:
    def __init__(self, path_to_the_file: str) -> None:
        try:
            with open(path_to_the_file, "r") as file:
                self.data = list(csv.DictReader(file))
                if not self.data:
                    raise Exception("файл пуст")
        except FileNotFoundError:
            raise Exception("файл не был найден")
    
    def get_data(self) -> List[Dict]:
        return self.data


class Filtrator:
    def filter_condition_parser(self, condition: str) -> Tuple[str, str, Union[str, float]]:
        result = re.split(r"(.+?)([><=]+)(.+)", condition)[1:-1]
        if not result:
            raise("неверный формат условия для фильтра")
        field, operator, value = result
        try:
            value = float(value)
        except ValueError:
            pass

        return field, operator, value
    
    def filter_data(self, data: List[Dict], condition: str) -> List[Dict]:
        field, operator, value = self.filter_condition_parser(condition)
        filtered_data = []
        if field not in data[0]:
            raise(f"поле '{field}' не найдено в данных")
        for item in data:
            if isinstance(value, float):
                if operator == ">" and float(item[field]) > value:
                    filtered_data.append(item)
                elif operator == "<" and float(item[field]) < value:
                    filtered_data.append(item)
                elif operator in ["=", "=="] and float(item[field]) == value:
                    filtered_data.append(item)
            elif operator in ["=", "=="] and item[field] == value:
                filtered_data.append(item)
        return filtered_data

class Aggregator:
    def aggregate_parser(self, condition: str) -> Tuple[str, str]:
        try:
            field, operation = condition.split("=")
        except:
            raise("неверный формат для aggregate")
        return field, operation

    def aggregate(self, data: List[Dict], condition: str) -> str:
        field, operation = self.aggregate_parser(condition)
        if field not in data[0]:
            raise(f"поле '{field}' не найдено в данных")
        try:
            values = [float(item[field]) for item in data]
        except ValueError:
            raise(f"поле '{field}' содержит нечисловые значения")
        count = 0
        if operation == "min":
            count = min(values)
        elif operation == "max":
            count = max(values)
        elif operation == "avg":
            count = sum(values) / len(values)
        else:
            raise("неверный оператор")
        result = [{operation: count}]
        return result


class Presenter:
    @staticmethod
    def print_data(data: List[Dict]) -> str:
        return tabulate(data, headers="keys", tablefmt="grid")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка CSV файлов с фильтрацией и агрегацией")
    parser.add_argument("--file", help="Путь к CSV файлу", required=True)
    parser.add_argument("--where", help="Условие фильтрации (например, 'age>30')")
    parser.add_argument("--aggregate", help="Агрегация данных (например, 'age=avg')")
    
