import csv
import argparse
import re
from tabulate import tabulate

class Reader:
    def __init__(self, path_to_the_file):
        with open(path_to_the_file, "r") as file:
            self.data = list(csv.DictReader(file))

    def filter_condition_parser(self, condition):
        try:
            result = re.split(r"(\w+)([><=]+)(\d+.\d+)", condition)[1:-1] # ['ratings', '==', '4.5'] ['name', '==', 'iphone 12']
            field, operator, value = result
            value = float(value)
        except:
            result = re.split(r"(\w+)([><=]+)(.+)", condition)[1:-1]
            field, operator, value = result
        return field, operator, value
    
    def _filter(self, condition):
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
    
    def agregate_parser(self, condition):
        result = re.split(r"(\w+)([><=]+)(\w+)", condition)[1:-1]
        field, _, maxminavg = result
        return field, maxminavg

    def agregate(self, condition):
        field, maxminavg = self.agregate_parser(condition)
        values = [float(item[field]) for item in self.data]
        count = 0
        if maxminavg == "min":
            cpunt = min(values)
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
'''
Reader("data.csv")._filter("brand>samsung") # не вызывается ошибка и программа продолжает работать
Reader("data.csv")._filter("brand=samsung") # корректно проверяется сохраняя типобезопасность(как и два ниже)
Reader("data.csv")._filter("price=299")
Reader("data.csv")._filter("rating>4.5")
Reader("data.csv").agregate("rating==avg")
'''