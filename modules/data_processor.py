import pandas as pd

def process_auction_data(data):
    """
    Обрабатывает данные о заявках на аукционы.
    :param data: DataFrame с данными.
    :return: Обработанный DataFrame.
    """
    result = pd.DataFrame(columns=['Год', 'Месяц', 'Статус', 'Количество'])

    for index, row in data.iterrows():
        status = row['статус']  # Статус (выиграно, проиграно и т.д.)
        year = row['год']  # Год

        for month in ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                      'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']:
            value = row[month]  # Количество заявок за месяц

            # Пропускаем пустые значения
            if pd.isna(value):
                continue

            # Преобразуем значение в число (если это возможно)
            try:
                value = int(value)
            except (ValueError, TypeError):
                # Если значение не может быть преобразовано в число, пропускаем его
                continue

            # Добавляем данные в результат
            new_row = pd.DataFrame({
                'Год': [year],
                'Месяц': f"{year}-{month}",  # Формат: "2017-январь"
                'Статус': [status],
                'Количество': [value]
            })
            result = pd.concat([result, new_row], ignore_index=True)

    return result