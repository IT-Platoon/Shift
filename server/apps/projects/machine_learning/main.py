"""Главный модуль подсистемы"""

import os

import pandas as pd

from .predict import predict_result_regression
from .utils import (
    get_report_dataframe,
    dataframe_to_json,
    get_tasks_and_names_json,
    save_predictions_to_txt,
    save_dataframe_xlsx,
    save_dataframe_csv,
)

DIR_NAME = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(DIR_NAME, 'model', 'xgboost_ensemble_full.pkl')
DATA_PATH = os.path.join(DIR_NAME, 'data_baseline', 'dataset_hackaton_ksg.csv')


def main(data_path):
    data_with_predict = predict_result_regression(MODEL_PATH, data_path)
    result = get_report_dataframe(
        data_with_predict,
        ['Кодзадачи', 'НазваниеЗадачи', 'predictions'],
    )
    save_dataframe_xlsx(data_with_predict)
    save_dataframe_csv(data_with_predict)
    save_predictions_to_txt(data_with_predict['predictions'])
    ended_json = dataframe_to_json(data_with_predict)
    ended_json["tasks"] = get_tasks_and_names_json(
        data_with_predict["Кодзадачи"],
        data_with_predict["НазваниеЗадачи"],
    )
    return ended_json


if __name__ == "__main__":
    main()
