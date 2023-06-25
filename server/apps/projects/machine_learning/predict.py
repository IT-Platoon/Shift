"""Модуль с финальной реализацией предсказания модели"""

import json
from pathlib import Path
from typing import Union

from .models import load_model_pycaret_regression, reg_predict
from .utils import load_data, preprocessing_data_shift


def predict_result_regression(path_to_model: Union[str, Path], path_to_data: Union[str, Path]) -> json:
    """
    Функция для предсказания результата входного файла

    :param path_to_model: Путь до файла с моделью
    :param path_to_data: Путь до файла с данными
    :return: Результат предсказания в формате json
    """
    data = load_data(path_to_data)

    preprocessed_data, lst = preprocessing_data_shift(data)

    model = load_model_pycaret_regression(path_to_model)

    # Предсказания должны быть целыми числами
    predictions = reg_predict(preprocessed_data, model).astype(int)

    data.insert(len(data.columns), 'predictions', predictions)
    data['predictions'] = data['predictions'].apply(lambda x: max(0, x))
    data['target'] = lst
    return data
