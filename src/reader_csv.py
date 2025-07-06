import csv
import argparse
import re
import sys
from typing import List, Dict, Tuple, Union, Optional
from tabulate import tabulate


class Reader:
    def __init__(self, path_to_the_file: str) -> None:
        try:
            with open(path_to_the_file, "r") as file:
                self.data = list(csv.DictReader(file))

                if not self.data:
                    print("файл пуст")
                    sys.exit(0)
                
        except FileNotFoundError:
            print("Файл не был найден")
            sys.exit(1)
    
    def get_data(self) -> List[Dict]:
        return self.data


class Filtrator:
    def filter_condition_parser(self, condition: str) -> Tuple[str, str, Union[str, float]]:
        result = re.split(r"(.+?)([><=]+)(.+)", condition)[1:-1]

        if not result:
            print("неверный формат для where")
            sys.exit(1)
        
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
            return f"Поле '{field}' не найдено в данных"
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
    def agregate_parser(self, condition: str) -> Tuple[str, str]:
        try:
            field, operation = condition.split("=")
        except:
            print("неверный формат для agregate")
            sys.exit(1)
        return field, operation

    def agregate(self, data: List[Dict], condition: str) -> str:
        field, operation = self.agregate_parser(condition)

        if field not in data[0]:
            print(f"Поле '{field}' не найдено в данных")
            sys.exit(1)
        try:
            values = [float(item[field]) for item in data]
        except ValueError:
            print(f"Поле '{field}' содержит нечисловые значения")
            sys.exit(0)
        count = 0
        if operation == "min":
            count = min(values)
        elif operation == "max":
            count = max(values)
        elif operation == "avg":
            count = sum(values) / len(values)
        else:
            return "такой операции в агрегации пока что не предусмотрено"
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
    
    args = parser.parse_args()
    
    # Чтение данных
    reader = Reader(args.file)
    data = reader.get_data()
    
    # Применение фильтрации, если указано
    if args.where:
        filtrator = Filtrator()
        data = filtrator.filter_data(data, args.where)
        if isinstance(data, str):  # Обработка ошибки из filter_data
            print(data)
            sys.exit(1)
    
    # Применение агрегации, если указано
    if args.aggregate:
        aggregator = Aggregator()
        result = aggregator.agregate(data, args.aggregate)
        if isinstance(result, str):  # Обработка ошибки из agregate
            print(result)
            sys.exit(1)
        data = result
    
    # Вывод результатов
    print(Presenter.print_data(data))
