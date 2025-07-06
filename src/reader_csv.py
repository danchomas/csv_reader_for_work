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
    
    def _filter(self, condition: str) -> str:
        field, operator, value = self.filter_condition_parser(condition)
        filtered_data = []
        if field not in self.data[0]:
            return f"Поле '{field}' не найдено в данных"
        for item in self.data:
            if isinstance(value, float):
                if operator == ">" and float(item[field]) > value:
                    filtered_data.append(item)
                elif operator == "<" and float(item[field]) < value:
                    filtered_data.append(item)
                elif operator in ["=", "=="] and float(item[field]) == value:
                    filtered_data.append(item)
            elif operator in ["=", "=="] and item[field] == value:
                filtered_data.append(item)
        self.data = filtered_data
        result = tabulate(filtered_data, headers='keys', tablefmt='grid')
        return result
    
    def agregate_parser(self, condition: str) -> Tuple[str, str]:
        try:
            field, operation = condition.split("=")
        except:
            print("неверный формат для agregate")
            sys.exit(1)
        return field, operation

    def agregate(self, condition: str) -> str:
        field, operation = self.agregate_parser(condition)

        if field not in self.data[0]:
            print(f"Поле '{field}' не найдено в данных")
            sys.exit(1)
        try:
            values = [float(item[field]) for item in self.data]
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
        data = [{operation: count}]
        return tabulate(data, headers='keys', tablefmt='grid')
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Пример использования argparse")
    parser.add_argument("--file", help="название датасета", required=True)
    parser.add_argument("--where", help="фильтр по колонкам")
    parser.add_argument("--agregate", help="агрегация")

    args = parser.parse_args()

    reader = Reader(args.file)
    print(reader._filter(args.where))
    print(reader.agregate(args.agregate))