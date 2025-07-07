import argparse
from reader import Reader
from filtrator import Filtrator
from aggregator import Aggregator
from presenter import Presenter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="путь к CSV файлу с данными", required=True)
    parser.add_argument("--where", help="условие фильтрации данных (например, 'price>100')", default=None)
    parser.add_argument("--aggregate", help="условие агрегации данных (например, 'rating=avg')", default=None)
    
    args = parser.parse_args()
    reader = Reader(args.file)
    data = reader.get_data()
    
    if args.where:
        filtrator = Filtrator()
        data = filtrator.filter_data(data, args.where)
    
    if args.aggregate:
        aggregator = Aggregator()
        result = aggregator.aggregate(data, args.aggregate)
        print(Presenter.print_data(result))
    else:
        print(Presenter.print_data(data))