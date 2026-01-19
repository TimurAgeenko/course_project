import json

from src.utils import (
    choose_greeting,
    get_cards_info,
    get_currency_rates,
    get_data,
    get_stock_prices,
    get_top_transactions,
    sort_data_by_date
)


def main_views(date: str, path: str = "../data/operations.xlsx") -> str:
    """Главная функция принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и путь до excel-файла, который по умолчанию находится в директории data в корне проекта, и возвращающая JSON-ответ"""
    raw_data = get_data(path)
    data = sort_data_by_date(raw_data, date)

    result = {
        "greeting": choose_greeting(date),
        "cards": get_cards_info(data),
        "top_transactions": get_top_transactions(data),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices()
    }

    result_json = json.dumps(result, ensure_ascii=False, indent=4)

    return result_json
