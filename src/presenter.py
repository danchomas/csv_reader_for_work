from tabulate import tabulate
from typing import List, Dict

class Presenter:
    @staticmethod
    def print_data(data: List[Dict]) -> str:
        return tabulate(data, headers="keys", tablefmt="grid")