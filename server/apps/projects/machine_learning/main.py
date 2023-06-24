"""Главный модуль подсистемы"""

import os

from .predict import predict_result_regression
from .utils import get_report_dataframe

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(DIR_NAME, 'model', 'test_model1.pkl')
DATA_PATH = os.path.join(DIR_NAME, 'data_baseline', 'dataset_hackaton_ksg.csv')


def main(data_path):
    data_with_predict = predict_result_regression(MODEL_PATH, data_path)
    result = get_report_dataframe(data_with_predict, ['Кодзадачи', 'НазваниеЗадачи', 'predictions'])
    print(result)


if __name__ == "__main__":
    main()
