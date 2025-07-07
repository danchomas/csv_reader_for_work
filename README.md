# csv_reader_for_work
Инструмент для обработки данных

Использование

    python3 main.py --file "data/data.csv"

С фильтрацией

    python3 main.py --file "data/data.csv" --where "brand=xiaomi"

С агрегацией

    python3 main.py --file "data/data.csv" --aggregate "price=max"


![изображение](https://github.com/user-attachments/assets/190c2a67-752e-4122-bbac-6da7f30075c3)



Комбинированный пример

    python3 main.py --file "data/data.csv" --where "brand=xiaomi" --aggregate "price=max"

Тестирование

Запуск тестов с отчетом о покрытии:

    pytest --cov=src --cov-report=html tests/

создается папка htmlcov, которая показывает данные о покрытии
