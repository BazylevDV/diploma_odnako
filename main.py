from modules.data_loader import load_auction_data
from modules.data_processor import process_auction_data
from modules.data_analyzer import analyze_data, plot_interactive_lineplot, plot_interactive_barplot, plot_interactive_heatmap, plot_interactive_piechart
from visualizations.plotter import plot_auction_data

# Загружаем данные
data = load_auction_data()
print("Загруженные данные:")
print(data)

# Обрабатываем данные
processed_data = process_auction_data(data)
print("Обработанные данные:")
print(processed_data)

# Визуализируем данные с помощью Matplotlib и Seaborn
plot_auction_data(processed_data)
analyze_data(processed_data, output_dir='visualizations')

# Визуализируем данные с помощью Plotly
plot_interactive_lineplot(processed_data)
plot_interactive_barplot(processed_data)
plot_interactive_heatmap(processed_data)
plot_interactive_piechart(processed_data)
