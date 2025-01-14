import unittest
import pandas as pd
import os
from modules.data_loader import load_auction_data
from modules.data_processor import process_auction_data

print("Текущая рабочая директория:", os.getcwd())

class TestDataProcessing(unittest.TestCase):
    """
    Тесты для проверки загрузки и обработки данных.
    """

    def test_data_loading(self):
        """
        Проверяем, что данные загружаются корректно.
        """
        data = load_auction_data()
        self.assertIsInstance(data, pd.DataFrame)  # Проверяем, что данные загружены в DataFrame
        self.assertFalse(data.empty)  # Проверяем, что DataFrame не пустой

    def test_data_processing(self):
        """
        Проверяем, что данные обрабатываются корректно.
        """
        data = load_auction_data()
        processed_data = process_auction_data(data)
        self.assertIsInstance(processed_data, pd.DataFrame)  # Проверяем, что данные обработаны в DataFrame
        self.assertFalse(processed_data.empty)  # Проверяем, что DataFrame не пустой
        # Проверяем, что все необходимые колонки присутствуют
        self.assertIn('Год', processed_data.columns)
        self.assertIn('Месяц', processed_data.columns)
        self.assertIn('Статус', processed_data.columns)
        self.assertIn('Количество', processed_data.columns)

    def test_visualization_files(self):
        """
        Проверяем, что файлы визуализации создаются корректно.
        """
        data = load_auction_data()
        processed_data = process_auction_data(data)

        # Проверяем, что файлы визуализации создаются
        from modules.data_analyzer import analyze_data
        analyze_data(processed_data, output_dir='visualizations')

        # Проверяем, что файлы существуют
        self.assertTrue(os.path.exists('visualizations/yearly_analysis.png'))
        self.assertTrue(os.path.exists('visualizations/monthly_analysis.png'))
        self.assertTrue(os.path.exists('visualizations/win_ratio_analysis.png'))
        self.assertTrue(os.path.exists('visualizations/heatmap_analysis.png'))
        self.assertTrue(os.path.exists('visualizations/rejected_analysis.png'))
        self.assertTrue(os.path.exists('visualizations/plotly_lineplot.html'))
        self.assertTrue(os.path.exists('visualizations/plotly_barplot.html'))
        self.assertTrue(os.path.exists('visualizations/plotly_heatmap.html'))
        self.assertTrue(os.path.exists('visualizations/plotly_piechart.html'))


if __name__ == '__main__':
    unittest.main()