import csv
from typing import List, Dict, Tuple, Union
from tabulate import tabulate
import pytest

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
    
