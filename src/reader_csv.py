import csv
import argparse
import re
from typing import List, Dict, Tuple, Union, Optional
from tabulate import tabulate

class Reader:
    def __init__(self, path_to_the_file: str) -> None:
        try:
            with open(path_to_the_file, "r") as file:
                self.data = list(csv.DictReader(file))
        except:
            raise ""

    def filter_condition_parser(self, condition: str) -> Tuple[str, str, Union[str, float]]:
        try:
            result = re.split(r"(\w+)([><=]+)(\d+.\d+)", condition)[1:-1] # ['ratings', '==', '4.5'] ['name', '==', 'iphone 12']
            field, operator, value = result
            value = float(value)
        except:
            result = re.split(r"(.+)([><=]+)(.+)", condition)[1:-1]
            field, operator, value = result
        return field, operator, value
    
    def _filter(self, condition: str) -> str:
        field, operator, value = self.filter_condition_parser(condition)
        filtered_data = []
        for item in self.data:
            if isinstance(value, float):
                if operator == ">" and float(item[field]) > value:
                    filtered_data.append(item)
                elif operator == "<" and float(item[field]) < value:
                    filtered_data.append(item)
                elif operator == "=" and float(item[field]) == value:
                    filtered_data.append(item)
            elif operator == "=" and item[field] == value:
                filtered_data.append(item)
        self.data = filtered_data
        result = tabulate(filtered_data, headers='keys', tablefmt='grid')
        return result
    
    def agregate_parser(self, condition: str) -> Tuple[str, str]:
        result = re.split(r"(.+)([><=]+)(.+)", condition)[1:-1]
        field, _, maxminavg = result
        return field, maxminavg

    def agregate(self, condition: str) -> str:
        field, maxminavg = self.agregate_parser(condition)
        values = [float(item[field]) for item in self.data]
        count = 0
        if maxminavg == "min":
            count = min(values)
        elif maxminavg == "max":
            count = max(values)
        elif maxminavg == "avg":
            count = sum(values) / len(values)
        data = [dict(field=count)]
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