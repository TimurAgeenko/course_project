import os
from unittest.mock import patch

from dotenv import load_dotenv

from src.utils import (
    choose_greeting,
    get_cards_info,
    get_currency_rates,
    get_data,
    get_stock_prices,
    get_top_transactions,
    sort_data_by_date
)


def test_choose_greeting():
    assert choose_greeting("18:30") == "Добрый вечер"
    assert choose_greeting("00:30") == "Доброй ночи"
    assert choose_greeting("06:30") == "Доброе утро"
    assert choose_greeting("12:30") == "Добрый день"
    assert choose_greeting("") == "Часы указаны в неверном формате, пожалуйста, укажите их в формате HH:MM:SS"


def test_get_data():
    data = get_data("./data/operations.xlsx")
    assert data[0]["Категория"] == "Супермаркеты"
    assert data[1]["Бонусы (включая кэшбэк)"] == 1


def test_get_data_not_exist():
    data = get_data("./data/operations_excel.xlsx")
    assert data == "File './data/operations_excel.xlsx' not found."


def test_sort_data_by_date():
    data = get_data("./data/operations.xlsx")
    assert sort_data_by_date(data, "2021-09-15")[0]["Номер карты"] == "*7197"


def test_sort_data_by_date_wrong_format():
    data = get_data("./data/operations.xlsx")
    assert (
        sort_data_by_date(data, "15-09-2021")
        == "Дата указана в неверном формате, пожалуйста, укажите её в формате YYYY-MM-DD"
    )


def test_get_cards_info():
    data = get_data("./data/operations.xlsx")
    data = sort_data_by_date(data, "2021-09-15")
    cards_info = get_cards_info(data)

    assert len(cards_info) == 2
    assert isinstance(cards_info[0]["last_digits"], str)
    assert len(cards_info[0]["last_digits"]) == 4
    assert isinstance(cards_info[0]["total_spent"], float)
    assert isinstance(cards_info[0]["cashback"], float)


def test_get_top_transactions():
    data = get_data("./data/operations.xlsx")
    data = sort_data_by_date(data, "2021-09-15")
    top_transactions = get_top_transactions(data)

    assert top_transactions[0] == {
        "date": "14.09.2021",
        "amount": 150000.0,
        "category": "Переводы",
        "description": "Перевод с карты",
    }
    assert top_transactions[4] == {
        "date": "09.09.2021",
        "amount": 1586.62,
        "category": "ЖКХ",
        "description": "ЖКУ Дом",
    }


@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {
        "success": True,
        "timestamp": 1767751863,
        "base": "USD",
        "date": "2026-01-07",
        "rates": {"RUB": 80.499355},
    }

    with open("./data/test_file", "w") as f:
        f.write('{"user_currencies": ["USD"]}')
    assert get_currency_rates("./data/test_file") == [{"currency": "USD", "rate": 80.5}]

    os.remove("./data/test_file")

    load_dotenv()
    api_key = os.getenv("CURRENCY_RATES_API_KEY")
    url = os.getenv("CURRENCY_RATES_URL")
    payload = {}
    headers = {"apikey": f"{api_key}"}
    params = {"symbols": "RUB", "base": "USD"}

    mock_get.assert_called_once_with(url, headers=headers, data=payload, params=params)


@patch("src.utils.get_currency_rates")
@patch("requests.get")
def test_get_stock_prices(mock_get, mock_currency_rates):
    mock_get.return_value.json.return_value = {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "AMZN",
            "3. Last Refreshed": "2026-01-08",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        "Time Series (Daily)": {
            "2026-01-08": {
                "1. open": "243.0600",
                "2. high": "246.4100",
                "3. low": "241.8800",
                "4. close": "246.2900",
                "5. volume": "39175991",
            }
        },
    }

    mock_currency_rates.return_value = [{"currency": "USD", "rate": 80.5}]

    with open("./data/test_file", "w") as f:
        f.write('{"user_currencies": ["USD"], "user_stocks": ["AMZN"]}')
    assert get_stock_prices("./data/test_file") == [{"stock": "AMZN", "rate": 19826.35}]

    os.remove("./data/test_file")

    load_dotenv()
    api_key = os.getenv("STOCK_PRICES_API_KEY")
    url = os.getenv("STOCK_PRICES_URL")
    params = {"function": "TIME_SERIES_DAILY", "symbol": "AMZN", "apikey": api_key}
    mock_get.assert_called_once_with(url, params=params)

    mock_currency_rates.assert_called_once_with("./data/test_file")
