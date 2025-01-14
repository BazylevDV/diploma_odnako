import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt



matplotlib.use('Agg')  # Используем бэкенд, который не требует Tcl/Tk


def plot_auction_data(data):
    """
    Визуализирует данные о заявках на аукционы и сохраняет график в файл.
    :param data: DataFrame с данными.
    """
    plt.figure(figsize=(14, 7))
    sns.lineplot(x='Месяц', y='Количество', hue='Статус', data=data)
    plt.title('Динамика заявок на аукционы (2017–2022)')
    plt.xlabel('Месяц')
    plt.ylabel('Количество')
    plt.xticks(rotation=90)  # Поворачиваем подписи по оси X на 90 градусов
    plt.grid(True)
    plt.tight_layout()  # Улучшаем расположение элементов

    # Сохраняем график в файл
    plt.savefig('auction_plot.png')
    print("График сохранен в файл 'auction_plot.png'")