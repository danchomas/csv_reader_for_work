# csv_reader_for_work
Инструмент для обработки данных
Использование
    python3 main.py --file "путь/к/файлу.csv"

С фильтрацией
    python3 main.py --file "data/data.csv" --where "brand=xiaomi"

С агрегацией
    python3 main.py --file "data/data.csv" --aggregate "price=max"

Комбинированный пример
    python3 main.py --file "data/data.csv" --where "brand=xiaomi" --aggregate "price=max"

Тестирование

Запуск тестов с отчетом о покрытии:
    pytest --cov=src --cov-report=html tests/

создается папка htmlcov, которая показывает данные о покрытии
