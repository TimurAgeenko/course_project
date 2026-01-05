import json
import os
import re

import pandas as pd


def choose_greeting(date: str) -> str:
    """Принимает строку с датой в формате YYYY-MM-DD HH:MM:SS
    и возвращает строку с приветствием, которая будет отличаться в зависимости от времени суток"""
    match = re.search(r"\d+:\d+:*\d*", date)
    result = ""
    if match:
        digits = re.findall(r"\d+", match.group(0))
        if 6 <= int(digits[0]) < 12:
            result = "Доброе утро"
        elif 12 <= int(digits[0]) < 18:
            result = "Добрый день"
        elif int(digits[0]) >= 18:
            result = "Добрый вечер"
        elif int(digits[0]) >= 0:
            result = "Доброй ночи"
    else:
        result = "Часы указаны в неверном формате, пожалуйста, укажите их в формате HH:MM:SS"

    return result


def get_data(path: str) -> list[dict] | str:
    """
    Принимает путь к файлу в формате xlsx, содержащий информацию о транзакциях,
    и возвращает список словарей с транзакциями.
    """
    if os.path.exists(path):
        if path.endswith(".xlsx"):
            df = pd.read_excel(path)
            data_json = df.to_json(orient="records")
            data = json.loads(data_json)
            return data
        else:
            return f"File '{path}' is not an excel file."
    else:
        return f"File '{path}' not found."


def sort_data_by_date(data: list[dict], date: str) -> list[dict] | str:
    """Принимает список словарей с транзакциями и дату в формате YYYY-MM-DD HH:MM:SS
    и возвращает отсортированный список словарей, где находятся транзакции с датой от начала месяца,
    на который выпадает указанная дата, до указанной даты"""
    match = re.search(r"\d{4}-\d{2}-\d{2}", date)
    result = []
    if match:
        digits = re.findall(r"\d+", match.group(0))
        for item in data:
            item_match = re.search(r"\d{2}\.\d{2}\.\d{4}", item["Дата операции"])
            item_digits = re.findall(r"\d+", item_match.group(0))
            if item_digits[0] <= digits[2] and item_digits[1] == digits[1] and item_digits[2] == digits[0]:
                result.append(item)
    else:
        return "Дата указана в неверном формате, пожалуйста, укажите её в формате YYYY-MM-DD"

    return result
