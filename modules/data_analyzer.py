import pandas as pd
import seaborn as sns
import plotly.express as px
import os
import matplotlib
matplotlib.use('Agg')  # Используем бэкенд, который не требует Tcl/Tk
import matplotlib.pyplot as plt


def analyze_data(data, output_dir='visualizations'):
    """
    Проводит анализ данных и сохраняет графики в указанную папку.
    :param data: DataFrame с данными.
    :param output_dir: Папка для сохранения графиков.
    """
    # Создаем папку для графиков, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Анализ по годам
    yearly_data = data.groupby(['Год', 'Статус'])['Количество'].sum().unstack()
    plt.figure(figsize=(12, 6))
    yearly_data.plot(kind='bar', stacked=True)
    plt.title('Количество заявок по годам и статусам')
    plt.xlabel('Год')
    plt.ylabel('Количество заявок')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'yearly_analysis.png'))
    plt.close()

    # 2. Анализ по месяцам
    monthly_data = data.groupby(['Месяц', 'Статус'])['Количество'].sum().unstack()
    plt.figure(figsize=(14, 7))
    monthly_data.plot(kind='line', marker='o')
    plt.title('Количество заявок по месяцам и статусам')
    plt.xlabel('Месяц')
    plt.ylabel('Количество заявок')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'monthly_analysis.png'))
    plt.close()

    # 3. Доля выигранных заявок
    win_loss_data = data[data['Статус'].isin(['выиграно', 'проиграно'])]
    win_loss_ratio = win_loss_data.groupby(['Год', 'Статус'])['Количество'].sum().unstack()
    win_loss_ratio['Доля выигранных'] = win_loss_ratio['выиграно'] / (
                win_loss_ratio['выиграно'] + win_loss_ratio['проиграно'])
    plt.figure(figsize=(10, 6))
    win_loss_ratio['Доля выигранных'].plot(kind='bar', color='skyblue')
    plt.title('Доля выигранных заявок по годам')
    plt.xlabel('Год')
    plt.ylabel('Доля выигранных заявок')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'win_ratio_analysis.png'))
    plt.close()

    # 4. Тепловая карта по месяцам и годам
    heatmap_data = data.pivot_table(index='Год', columns='Месяц', values='Количество', aggfunc='sum')
    heatmap_data = heatmap_data.apply(pd.to_numeric, errors='coerce')
    heatmap_data = heatmap_data.dropna(how='all', axis=0).dropna(how='all', axis=1)
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f', linewidths=.5)
    plt.title('Тепловая карта заявок по годам и месяцам')
    plt.xlabel('Месяц')
    plt.ylabel('Год')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'heatmap_analysis.png'))
    plt.close()

    # 5. Анализ отклоненных заявок
    rejected_data = data[data['Статус'] == 'отклонено по первой части']
    rejected_yearly = rejected_data.groupby('Год')['Количество'].sum()
    plt.figure(figsize=(10, 6))
    rejected_yearly.plot(kind='bar', color='orange')
    plt.title('Количество отклоненных заявок по годам')
    plt.xlabel('Год')
    plt.ylabel('Количество отклоненных заявок')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rejected_analysis.png'))
    plt.close()

    # 6. Интерактивный линейный график
    plot_interactive_lineplot(data, output_dir)

    # 7. Интерактивная столбчатая диаграмма
    plot_interactive_barplot(data, output_dir)

    # 8. Интерактивная тепловая карта
    plot_interactive_heatmap(data, output_dir)

    # 9. Интерактивная круговая диаграмма
    plot_interactive_piechart(data, output_dir)

    print(f"Графики сохранены в папку '{output_dir}'")


def plot_interactive_lineplot(data, output_dir='visualizations'):
    """
    Создает интерактивный линейный график с использованием Plotly.
    :param data: DataFrame с данными.
    :param output_dir: Папка для сохранения графика.
    """
    # Фильтруем данные для статусов "выиграно" и "проиграно"
    filtered_data = data[data['Статус'].isin(['выиграно', 'проиграно'])]

    # Проверяем данные
    print("Данные для интерактивного линейного графика:")
    print(filtered_data.head())

    # Строим график
    try:
        fig = px.line(filtered_data, x='Год', y='Количество', color='Статус', markers=True,
                      title='Количество заявок по годам (Plotly)')
        fig.update_layout(xaxis_title='Год', yaxis_title='Количество заявок')

        # Сохраняем график
        fig.write_html(os.path.join(output_dir, 'plotly_lineplot.html'))
        print("Интерактивный линейный график сохранен в файл 'plotly_lineplot.html'")
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")


def plot_interactive_barplot(data, output_dir='visualizations'):
    """
    Создает интерактивную столбчатую диаграмму с использованием Plotly.
    :param data: DataFrame с данными.
    :param output_dir: Папка для сохранения графика.
    """
    # Группируем данные по годам и статусам
    yearly_data = data.groupby(['Год', 'Статус'])['Количество'].sum().unstack().reset_index()

    # Проверяем данные
    print("Данные для интерактивной столбчатой диаграммы:")
    print(yearly_data.head())

    # Строим график
    try:
        fig = px.bar(yearly_data, x='Год', y=['выиграно', 'проиграно'], barmode='group',
                     title='Количество заявок по годам (Plotly)')
        fig.update_layout(xaxis_title='Год', yaxis_title='Количество заявок', legend_title='Статус')

        # Сохраняем график
        fig.write_html(os.path.join(output_dir, 'plotly_barplot.html'))
        print("Интерактивная столбчатая диаграмма сохранена в файл 'plotly_barplot.html'")
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")


def plot_interactive_heatmap(data, output_dir='visualizations'):
    """
    Создает интерактивную тепловую карту с использованием Plotly.
    :param data: DataFrame с данными.
    :param output_dir: Папка для сохранения графика.
    """
    # Преобразуем данные для тепловой карты
    heatmap_data = data.pivot_table(index='Год', columns='Месяц', values='Количество', aggfunc='sum')

    # Проверяем, что данные содержат только числа
    heatmap_data = heatmap_data.apply(pd.to_numeric, errors='coerce')

    # Удаляем строки и столбцы, где все значения NaN
    heatmap_data = heatmap_data.dropna(how='all', axis=0).dropna(how='all', axis=1)

    # Проверяем данные
    print("Данные для интерактивной тепловой карты:")
    print(heatmap_data.head())

    # Строим график
    try:
        fig = px.imshow(heatmap_data, labels=dict(x="Месяц", y="Год", color="Количество"),
                        x=heatmap_data.columns, y=heatmap_data.index, color_continuous_scale='YlGnBu',
                        title='Тепловая карта заявок по годам и месяцам (Plotly)')
        fig.update_layout(xaxis_title='Месяц', yaxis_title='Год')

        # Сохраняем график
        fig.write_html(os.path.join(output_dir, 'plotly_heatmap.html'))
        print("Интерактивная тепловая карта сохранена в файл 'plotly_heatmap.html'")
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")


def plot_interactive_piechart(data, output_dir='visualizations'):
    """
    Создает интерактивную круговую диаграмму с использованием Plotly.
    :param data: DataFrame с данными.
    :param output_dir: Папка для сохранения графика.
    """
    # Фильтруем данные для статусов "выиграно" и "проиграно"
    win_loss_data = data[data['Статус'].isin(['выиграно', 'проиграно'])]

    # Считаем общее количество выигранных и проигранных заявок
    total_wins = win_loss_data[win_loss_data['Статус'] == 'выиграно']['Количество'].sum()
    total_losses = win_loss_data[win_loss_data['Статус'] == 'проиграно']['Количество'].sum()

    # Проверяем данные
    print("Данные для интерактивной круговой диаграммы:")
    print(f"Выиграно: {total_wins}, Проиграно: {total_losses}")

    # Строим график
    try:
        fig = px.pie(values=[total_wins, total_losses], names=['Выиграно', 'Проиграно'],
                     title='Доля выигранных и проигранных заявок (Plotly)')

        # Сохраняем график
        fig.write_html(os.path.join(output_dir, 'plotly_piechart.html'))
        print("Интерактивная круговая диаграмма сохранена в файл 'plotly_piechart.html'")
    except Exception as e:
        print(f"Ошибка при создании графика: {e}")