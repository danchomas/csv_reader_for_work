# csv_reader_for_work
Инструмент для обработки данных

Использование

    python3 main.py --file "data/data.csv"


![изображение](https://github.com/user-attachments/assets/afd89882-de8f-46f4-a185-5f27e5eb4813)



С фильтрацией

    python3 main.py --file "data/data.csv" --where "brand=xiaomi"


![изображение](https://github.com/user-attachments/assets/0227c251-b6fa-4f27-b5a9-60b6db6224f9)



С агрегацией

    python3 main.py --file "data/data.csv" --aggregate "price=max"


![изображение](https://github.com/user-attachments/assets/190c2a67-752e-4122-bbac-6da7f30075c3)



Комбинированный пример

    python3 main.py --file "data/data.csv" --where "brand=xiaomi" --aggregate "price=max"


![изображение](https://github.com/user-attachments/assets/751b1e26-dd37-4926-82ba-75ee0a1919ca)



Тестирование

Запуск тестов с отчетом о покрытии:

    pytest --cov=src --cov-report=html tests/


![изображение](https://github.com/user-attachments/assets/595a4b52-58a4-4e2d-8c4d-3df517fdc6e1)



создается папка htmlcov, которая показывает данные о покрытии
покрывается не весь код, но все классы без main. до добавления было 100 процентов
