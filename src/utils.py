import datetime as dt
import json
import os
import re

import pandas as pd
import requests
from dotenv import load_dotenv


def choose_greeting() -> str:
    """Возвращает строку с приветствием, которая будет отличаться в зависимости от времени суток"""
    result = ""

    user_time = dt.datetime.now().strftime("%H:%M:%S")
    digits = re.findall(r"\d+", user_time)

    if 6 <= int(digits[0]) < 12:
        result = "Доброе утро"
    elif 12 <= int(digits[0]) < 18:
        result = "Добрый день"
    elif int(digits[0]) >= 18:
        result = "Добрый вечер"
    elif int(digits[0]) >= 0:
        result = "Доброй ночи"

    return result


def get_data(path: str = "../data/operations.xlsx") -> list[dict] | str:
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
    result = []

    date_match = re.search(r"\d{4}-\d{2}-\d{2}", date)
    time_match = re.search(r"\d+:\d+:\d+", date)

    if date_match and time_match:
        date_list_str = re.findall(r"\d+", date_match.group(0))
        time_list_str = re.findall(r"\d+", time_match.group(0))
        date_digits = [int(digit) for digit in date_list_str]
        time_digits = [int(digit) for digit in time_list_str]
        for item in data:
            item_date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", item["Дата операции"])
            item_time_match = re.search(r"\d+:\d+:\d+", item["Дата операции"])
            item_date_list_str = re.findall(r"\d+", item_date_match.group(0))
            item_time_list_str = re.findall(r"\d+", item_time_match.group(0))
            item_date_digits = [int(digit) for digit in item_date_list_str]
            item_time_digits = [int(digit) for digit in item_time_list_str]
            if (
                item_date_digits[0] <= date_digits[2]
                and item_date_digits[1] == date_digits[1]
                and item_date_digits[2] == date_digits[0]
            ):
                if item_time_digits[0] < time_digits[0]:
                    result.append(item)
                elif item_time_digits[0] == time_digits[0] and item_time_digits[1] < time_digits[1]:
                    result.append(item)
                elif (
                    item_time_digits[0] == time_digits[0]
                    and item_time_digits[1] == time_digits[1]
                    and item_time_digits[2] <= time_digits[2]
                ):
                    result.append(item)
    else:
        return "Дата указана в неверном формате, пожалуйста, укажите её в формате YYYY-MM-DD HH:MM:SS"

    return result


def get_cards_info(data: list[dict]) -> list[dict]:
    """Принимает на вход список словарей с транзакциями и возвращает список словарей
    с использованными в транзакциях картами, в котором содержатся последние цифры карт,
    общая сумма потраченных денег и сумма кэшбэка"""
    cards_info = []
    cards_set = set()

    [cards_set.add(item["Номер карты"]) for item in data if item["Номер карты"]]

    [cards_info.append({"last_digits": card[1:], "total_spent": 0}) for card in cards_set]

    for item in data:
        for card in cards_info:
            if item["Номер карты"]:
                if item["Номер карты"][1:] == card["last_digits"]:
                    if item["Сумма операции"] < 0:
                        card["total_spent"] += abs(item["Сумма операции"])
            card["cashback"] = round((card["total_spent"] / 100), 2)

    return cards_info


def get_top_transactions(data: list[dict]) -> list[dict]:
    """Принимает на вход список словарей с транзакциями и возвращает список словарей
    с наибольшими по сумме транзакциями с информацией о дате операции, её сумме, категории и описании"""
    top_transactions = []
    sorted_data = sorted(data, key=lambda x: x["Сумма операции"])
    sorted_info = []
    for item in sorted_data:
        if item["Статус"] == "OK":
            sorted_info.append(item)

    for item in sorted_info[:5]:
        top_transactions.append(
            {
                "date": item["Дата операции"][:10],
                "amount": abs(item["Сумма операции"]),
                "category": item["Категория"],
                "description": item["Описание"],
            }
        )

    return top_transactions


def get_currency_rates(path: str = "../user_settings.json") -> list[dict]:
    """Принимает на вход путь до файла с кодами валют и акций, заданными пользователем,
    который по умолчанию находится в корне проекта,
    и возвращает список словарей с кодом валюты и её стоимостью в рублях"""
    currency_rates = []

    with open(path) as f:
        data = json.load(f)
    user_currencies = data["user_currencies"]

    load_dotenv()
    api_key = os.getenv("CURRENCY_RATES_API_KEY")
    url = os.getenv("CURRENCY_RATES_URL")
    payload = {}
    headers = {"apikey": f"{api_key}"}

    for currency in user_currencies:
        params = {"symbols": "RUB", "base": f"{currency}"}
        response = requests.get(url, headers=headers, data=payload, params=params)
        result = response.json()
        currency_rates.append({"currency": currency, "rate": round(result["rates"]["RUB"], 2)})

    return currency_rates


def get_stock_prices(path: str = "../user_settings.json") -> list[dict]:
    """Принимает на вход путь до файла с кодами валют и акций, заданными пользователем,
    который по умолчанию находится в корне проекта,
    и возвращает список словарей с кодом валюты и её стоимостью в рублях"""
    stock_prices = []

    with open(path) as f:
        data = json.load(f)
    user_stocks = data["user_stocks"]

    load_dotenv()
    api_key = os.getenv("STOCK_PRICES_API_KEY")
    url = os.getenv("STOCK_PRICES_URL")

    currency_rates = get_currency_rates(path)
    usd_rate = [currency["rate"] for currency in currency_rates if currency["currency"] == "USD"][0]

    for stock in user_stocks:
        params = {"function": "TIME_SERIES_DAILY", "symbol": stock, "apikey": api_key}
        response = requests.get(url, params=params)
        result = response.json()
        if "Meta Data" in result:
            last_refresh_date = result["Meta Data"]["3. Last Refreshed"]
        if "Time Series (Daily)" in result:
            rate = float(result["Time Series (Daily)"][last_refresh_date]["4. close"])

        stock_prices.append({"stock": stock, "rate": round(rate * usd_rate, 2)})

    return stock_prices
