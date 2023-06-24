"""Файл с реализацией загрузки различных моделей"""

import os
from pathlib import Path
from typing import Union

import pandas as pd
import numpy as np
from pycaret.classification import load_model as load_classification_model
from pycaret.regression import load_model as load_regression_model

from .utils import check_path


def load_model_pycaret_classification(path_to_model: Union[str, Path]):
    """
    Загрузка модели классификации Pycaret.

    :param path_to_model: Путь до модели
    :return: Модель классификации Pycaret
    """
    if not check_path(path_to_model):
        raise FileNotFoundError('Неверный путь файла с моделью')

    path_sep = os.path.sep
    path_parts = str(path_to_model).split(path_sep)
    filename = '.'.join(path_parts[-1].split('.')[:-1])
    path_parts[0] = path_parts[0] + path_sep
    model_path = os.path.join(*path_parts[:-1], filename)

    loaded_model = load_classification_model(model_path)
    return loaded_model


def load_model_pycaret_regression(path_to_model: Union[str, Path]):
    """
    Загрузка модели регрессии Pycaret

    :param path_to_model: Путь до модели
    :return: Модель регрессии Pycaret
    """
    if not check_path(path_to_model):
        raise FileNotFoundError('Неверный путь файла с моделью')

    path_sep = os.path.sep
    path_parts = str(path_to_model).split(path_sep)
    filename = '.'.join(path_parts[-1].split('.')[:-1])
    path_parts[0] = path_parts[0] + path_sep
    model_path = os.path.join(*path_parts[:-1], filename)

    loaded_model = load_regression_model(model_path)
    return loaded_model


def clf_predict(data: pd.DataFrame, model) -> np.array:
    """
    Предсказание результата с помощью модели для классификации

    :param data: Данные, для которых нужно предсказать результат
    :param model: Модель классификации для создания предсказаний
    :return: Результат предсказания модели
    """
    return model.predict(data)


def reg_predict(data: pd.DataFrame, model) -> np.array:
    """
    Предсказание результата с помощью модели для регрессии

    :param data: Данные, для которых нужно предсказать результат
    :param model: Модель регрессии для создания предсказаний
    :return: Результат предсказания модели
    """
    return model.predict(data)


def ensemble(data: pd.DataFrame, models: list) -> np.array:
    """ Функция предсказания результата на основе N моделей.
    data: DataFrame - данные, для которых нужно предсказать результат.
    models: list - список моделей, которые участвуют в ансамбле.
    return: array - результат предсказания ансамбля моделей."""

    # TODO: Нужно придумать алгоритм, который на основе N результатов
    # выдаёт 1 результат.
    # Например, искать среднее значение у всех моделей и выдавать его за
    # результат.
