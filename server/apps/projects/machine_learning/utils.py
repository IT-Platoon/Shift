"""В этом файле реализованы функции сопровождения возможностей подсистемы"""

import json
from pathlib import Path
from typing import Optional, Union, Callable

import pandas as pd


def check_path(file_path: Union[str, Path]):
    """
    Проверка существования файла

    :param file_path: Путь до файла
    :return: True, если файл по указанному пути существует. Иначе False
    """
    return Path(file_path).exists()


def dataframe_to_json(data: pd.DataFrame) -> json:
    """ Преобразование dataframe в json-формат.
    data: DataFrame - таблица данных.
    return: json """


def get_report_dataframe(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Создание фрейма данных для отчёта

    :param df: Фрейм данных pandas
    :param columns: Колонки, которые используются в отчёте
    :return: Фрейм данных pandas только с нужными колонками
    """
    return df[columns]


def preprocessing_data_shift(df: pd.DataFrame) -> pd.DataFrame:
    """
    Обработка фрейма данных для использования в модели

    :param df: Фрейм данных pandas
    :return: Обработанный для использования в модели фрейм данных pandas
    """
    df = df.rename(columns={
        "№ п/п": "num",
        "Кодзадачи": "codeTask",
        "НазваниеЗадачи": "nameTask",
        "ПроцентЗавершенияЗадачи": "percent",
        "ДатаНачалаЗадачи": "dateStartWork",
        "ДатаОкончанияЗадачи": "dateEndWork",
        "ДатаначалаБП0": "dateStartPlan",
        "ДатаокончанияБП0": "dateEndPlan",
        "Статуспоэкспертизе": "statusExperts",
        "Экспертиза": "expert",
    })

    df['dateStartWork'] = pd.to_datetime(df['dateStartWork'])
    df['dateEndWork'] = pd.to_datetime(df['dateEndWork'])
    df['dateStartPlan'] = pd.to_datetime(df['dateStartPlan'])
    df['dateEndPlan'] = pd.to_datetime(df['dateEndPlan'])
    df['date_report'] = pd.to_datetime(df['date_report'])
    df["obj_key"] = df["obj_key"].astype("category")

    df['season'] = df['dateStartWork'].dt.month % 12 // 3 + 1
    df["season"] = df["season"].astype("category")

    lst = []
    for index, row in df.iterrows():
        shift = row['dateEndWork'] - row['dateStartWork']
        lst.append(shift.days)
    df['target'] = lst

    df = df.drop(columns=['dateEndWork', 'Unnamed: 0'])
    df = df[['obj_key', 'codeTask', 'nameTask', 'percent']]
    return df


def load_data(path: Union[str, Path]) -> pd.DataFrame:
    """
    Загрузка данных для модели

    :param path: Путь к файлу с данными
    :return: Фрейм данных pandas
    """
    if not check_path(path):
        raise FileNotFoundError('Неверный путь файла с данными')
    file_extension = str(path).split('\\')[-1].split('.')[-1]
    if file_extension in ['csv']:
        data = load_csv(path)
    elif file_extension in ['xls', 'xlsx']:
        data = load_excel(path)
    else:
        raise ValueError('Неверное расширение файла')
    return data


def load_csv(file_path: Union[str, Path],
             sep: str = ';', encoding: str = 'utf-8',
             encoding_errors: str = 'ignore',
             on_bad_lines: Union[str, Callable] = 'skip') -> pd.DataFrame:
    """
    Загрузка csv-файла и его преобразование в фрейм данных.

    Параметры sep и encoding необходимы для настройки обработки содержимого,
    а параметры encoding_errors и on_bad_lines - для обработки ошибок

    :param file_path: Путь до csv-файла
    :param sep: Разделитель
    :param encoding: Кодировка файла
    :param encoding_errors: Обработка ошибок кодирования
    :param on_bad_lines: Действия при обнаружении неправильной строки
                         (строка со слишком большим количеством полей)
    :return: Фрейм данных pandas
    """
    df = pd.read_csv(
        filepath_or_buffer=file_path,
        sep=sep,
        encoding=encoding,
        encoding_errors=encoding_errors,
        on_bad_lines=on_bad_lines,
    )
    return df


def load_excel(file_path: Union[str, Path],
               sheet_name: Optional[Union[str, int, list]] = None) -> pd.DataFrame:
    """
    Загрузка excel-файла и его преобразование в фрейм данных.

    :param file_path: Путь до excel-файла
    :param sheet_name: Название необходимых листов
    :return: Фрейм данных pandas
    """
    df = pd.read_excel(
        io=file_path,
        sheet_name=sheet_name,
        engine="openpyxl",
    )
    return df
