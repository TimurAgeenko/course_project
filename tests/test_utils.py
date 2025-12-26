from src.utils import choose_greeting

def test_choose_greeting():
    assert choose_greeting("18:30") == "Добрый вечер"
    assert choose_greeting("00:30") == "Доброй ночи"
    assert choose_greeting("06:30") == "Доброе утро"
    assert choose_greeting("12:30") == "Добрый день"
    assert choose_greeting("") == "Часы указаны в неверном формате, пожалуйста, укажите их в формате HH:MM:SS"
