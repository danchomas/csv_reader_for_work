import csv
import argparse
import re

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
        for item in self.data:
            try:
                float_item_field = float(item[field])
                if operator == ">" and float_item_field > value:
                    print(list(item.values()))
                elif operator == "<" and float_item_field < value:
                    print(list(item.values()))
                elif operator in ("=", "==") and float_item_field == value:
                    print(list(item.values()))
            except:
                continue
            if operator in ("=", "==") and item[field] == value:
                print(list(item.values()))
    

Reader("data.csv")._filter("brand>samsung")
Reader("data.csv")._filter("brand=samsung")
Reader("data.csv")._filter("price=299")
Reader("data.csv")._filter("rating>4.5")