"""В этом файле реализованы функции сопровождения возможностей подсистемы"""

import json
from pathlib import Path
from typing import Optional, Union, Callable, Hashable

import pandas as pd


def check_path(file_path: Union[str, Path]) -> bool:
    """
    Проверка существования файла

    :param file_path: Путь до файла
    :return: True, если файл по указанному пути существует. Иначе False
    """
    return Path(file_path).exists()


def dataframe_to_json(df: pd.DataFrame) -> dict:
    """
    Преобразование фрейма данных с предсказаниями в json-формат для
    отображения графиков

    :param df: Фрейм данных pandas
    :return: json-строка, содержащая в себе информацию для вывод информации
             о графиках
    """
    to_json = {'labels': df['Кодзадачи'].tolist(),
               'datasets': [{'data': df['target'].tolist(),
                             'label': 'Срок выполнения',
                             'type': 'line',
                             },
                            {'data': df['predictions'].tolist(),
                             'label': 'Предсказания сдвига',
                             'type': 'line',
                             }]
               }
    return to_json


def is_jsonable(x) -> bool:
    """
    Проверка объекта на возможность сериализации

    :param x: Объект для проверки
    :return: True, если объект можно сериализовать. Иначе False
    """
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def get_columns_json(kv: dict[str, pd.Series]) -> json:
    """
    Преобразование словаря в json-строку

    :param kv: Словарь для преобразования
    :return: json-представление словаря
    """
    to_json = {}
    for key, value in kv.items():
        value = value.tolist()
        if isinstance(key, Hashable) and is_jsonable(value):
            to_json[key] = value
    json_str = json.dumps(to_json)
    return json_str


def get_column_json(key: str, value: pd.Series) -> json:
    """
    Создание json-строки из одного объекта Series

    :param key: Ключ к json-представлению объекта
    :param value: Объект Series
    :return: json-строка, содержащая объект
    """
    pred_lst = value.tolist()
    to_json = {key: pred_lst}
    json_str = json.dumps(to_json)
    return json_str


def get_tasks_and_names_json(tasks: pd.Series, names: pd.Series) -> dict:
    """
    Форматирование кодов задач и их названий из Series в dict

    :param tasks: Коды задач в виде Series
    :param names: Названия задач в виде Series
    :return: dict с кодами задач и их названиями
    """
    tasks_lst, names_lst = tasks.tolist(), names.to_list()
    to_json = {'task_codes': tasks_lst, 'task_names': names_lst}
    return to_json


def save_predictions_to_txt(predictions: pd.Series,
                            filename: str = 'shift_predictions.txt') -> None:
    """
    Сохранение предсказаний в txt файл

    :param predictions: Результаты работы модели
    :param filename: Название файла, в который нужно сохранить результаты
    :return: None
    """
    pred_list = predictions.tolist()
    with open(filename, 'w', encoding='utf-8') as file:
        for prediction in pred_list:
            file.write(str(prediction) + '\n')


def get_report_dataframe(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Создание фрейма данных для отчёта

    :param df: Фрейм данных pandas
    :param columns: Колонки, которые используются в отчёте
    :return: Фрейм данных pandas только с нужными колонками
    """
    return df[columns]


def save_dataframe_xlsx(df: pd.DataFrame,
                        filename: str = 'report.xlsx') -> None:
    """
    Сохранение фрейма данных в файл с расширением .xlsx

    :param df: Фрейм данных pandas
    :param filename: Название файла сохранения
    :return: None
    """
    report = get_report_dataframe(df,
                                  ['Кодзадачи', 'НазваниеЗадачи', 'predictions'])
    report = report.rename(columns={
        "predictions": "Кол-во дней",
        "НазваниеЗадачи": "Название задачи",
    })
    report.to_excel(excel_writer=filename, index=False)


def save_dataframe_csv(df: pd.DataFrame,
                       filename: str = 'report.csv') -> None:
    """
    Сохранение фрейма данных в файл с расширением .csv

    :param df: Фрейм данных pandas
    :param filename: Название файла сохранения
    :return: None
    """
    report = get_report_dataframe(df,
                                  ['Кодзадачи', 'НазваниеЗадачи', 'predictions'])
    report = report.rename(columns={
        "predictions": "Кол-во дней",
        "НазваниеЗадачи": "Название задачи",
    })
    report.to_csv(path_or_buf=filename, sep=';', index=False)


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
    df = df.assign(date_report='2023.06.19')

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
        if not isinstance(shift, int):
            lst.append(shift.days)
        else:
            lst.append(0)

    df = df.drop(columns=['dateEndWork', 'obj_shortName'])
    # df = df[['obj_key', 'codeTask', 'nameTask', 'percent']]
    return df, lst


def load_data(path: Union[str, Path]) -> pd.DataFrame:
    """
    Загрузка данных для модели

    :param path: Путь к файлу с данными
    :return: Фрейм данных pandas
    """
    if not check_path(path):
        raise FileNotFoundError('Неверный путь файла с данными')
    file_extension = str(path).split('\\')[-1].split('.')[-1]
    if file_extension == 'csv':
        data = load_csv(path)
    elif file_extension == 'xls':
        data = load_xls(path)
    elif file_extension == 'xlsx':
        data = load_xlsx(path)
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


def load_xls(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Загрузка excel-файла и его преобразование в фрейм данных.

    Работа функции затрагивает только 1-й лист файла

    :param file_path: Путь до excel-файла
    :return: Фрейм данных pandas
    """
    df = pd.read_excel(
        io=file_path,
    )
    return df


def load_xlsx(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Загрузка excel-файла и его преобразование в фрейм данных.

    Работа функции затрагивает только 1-й лист файла

    :param file_path: Путь до excel-файла
    :return: Фрейм данных pandas
    """
    df = pd.read_excel(
        io=file_path,
        engine='openpyxl',
    )
    return df
