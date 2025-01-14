import os
import pandas as pd

def load_auction_data():
    """
    Загружает данные о заявках на аукционы из CSV-файла.
    :return: DataFrame с данными.
    """
    # Абсолютный путь к файлу
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Директория, где находится data_loader.py
    file_path = os.path.join(base_dir, '..', 'data', 'auctions_data.csv')  # Переход на уровень выше и в папку data

    # Выводим текущую рабочую директорию и путь к файлу
    print("Текущая рабочая директория:", os.getcwd())
    print("Путь к файлу:", file_path)

    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден!")

    # Читаем файл с заголовками
    df = pd.read_csv(file_path, encoding='utf-8')

    # Проверяем, не пустой ли DataFrame
    if df.empty:
        raise ValueError("Файл пуст или не содержит данных!")

    # Удаляем строки, где все значения NaN
    df = df.dropna(how='all')

    # Удаляем строки, где первый столбец равен 'статус' (повторяющиеся заголовки)
    df = df[df.iloc[:, 0] != 'статус']

    # Устанавливаем заголовки
    df.columns = ['статус', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                  'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь', 'год']

    # Сбрасываем индексы
    df = df.reset_index(drop=True)

    # Проверяем, есть ли NaN в данных
    print("Проверка на NaN в данных:")
    print(df.isna().sum())

    return df