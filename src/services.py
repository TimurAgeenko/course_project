import json
import re


def get_top_cashback_categories(data: list[dict], year: int, month: int) -> str:
    """Принимает на вход список словарей с транзакциями, год и месяц и возвращает
    JSON-строку с категориями, по которым был получен кэшбэк за указанный месяц и год, по убыванию."""
    categories_set = set()
    unnecessary_categories = [
        "Переводы",
        "Пополнения",
        "Другое",
        "Бонусы",
        "Услуги банка",
        "Сервис",
        "ЖКХ",
        "НКО",
        "Наличные",
        "Госуслуги",
    ]
    sorted_data = []
    categories_dict = {}

    for item in data:
        item_date_match = re.search(r"\d{2}\.\d{2}\.\d{4}", item["Дата операции"])
        item_date_list_str = re.findall(r"\d+", item_date_match.group(0))
        item_date_digits = [int(digit) for digit in item_date_list_str]
        if item_date_digits[2] == year and item_date_digits[1] == month:
            sorted_data.append(item)

    [categories_set.add(item["Категория"]) for item in sorted_data if item["Категория"] not in unnecessary_categories]

    for category in categories_set:
        categories_dict[category] = 0

    for item in sorted_data:
        if item["Категория"] in categories_set:
            categories_dict[item["Категория"]] += abs(item["Сумма операции"])

    result = dict(sorted(categories_dict.items(), key=lambda item: item[1], reverse=True))

    for key, value in result.items():
        result[key] = round(value / 100, 2)

    result_json = json.dumps(result, ensure_ascii=False, indent=4)

    return result_json
