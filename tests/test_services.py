from src.services import get_top_cashback_categories
from src.utils import get_data


def test_cashback_categories():
    data = get_data("./data/operations.xlsx")
    cashback_categories = get_top_cashback_categories(data, 2021, 12)

    assert cashback_categories == (
        "{\n"
        '    "Каршеринг": 112.72,\n'
        '    "Дом и ремонт": 60.77,\n'
        '    "Супермаркеты": 56.71,\n'
        '    "Фастфуд": 39.93,\n'
        '    "Ж/д билеты": 36.61,\n'
        '    "Электроника и техника": 34.99,\n'
        '    "Развлечения": 34.0,\n'
        '    "Различные товары": 18.06,\n'
        '    "Местный транспорт": 16.6,\n'
        '    "Аптеки": 14.11,\n'
        '    "Канцтовары": 7.1,\n'
        '    "Цветы": 6.0,\n'
        '    "Одежда и обувь": 5.25,\n'
        '    "Такси": 4.54,\n'
        '    "Связь": 3.45,\n'
        '    "Топливо": 2.25,\n'
        '    "Транспорт": 1.15,\n'
        '    "Детские товары": 0.28,\n'
        '    "Косметика": 0.15\n'
        "}"
    )
