# csv_reader_for_work
Инструмент для обработки данных

Этот проект предоставляет инструменты для чтения, фильтрации, агрегации и представления данных из CSV-файлов.
Возможности

    Чтение CSV-файлов с проверкой данных

    Фильтрация данных с использованием операторов сравнения (>, <, =)

    Агрегация данных с операциями (min, max, avg)

    Вывод результатов в форматированных таблицах

Установка
bash

pip install -r requirements.txt

Использование
Базовая команда
bash

python3 main.py --file "путь/к/файлу.csv"

С фильтрацией
bash

python3 main.py --file "data/data.csv" --where "brand=xiaomi"

С агрегацией
bash

python3 main.py --file "data/data.csv" --aggregate "price=max"

Комбинированный пример
bash

python3 main.py --file "data/data.csv" --where "brand=xiaomi" --aggregate "price=max"

Тестирование

Запуск тестов с отчетом о покрытии:
bash

pytest --cov=src --cov-report=html tests/

Эта команда создаст HTML-отчет о покрытии кода тестами.
