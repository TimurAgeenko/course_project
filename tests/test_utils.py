from src.utils import choose_greeting, get_data


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
