import re


def choose_greeting(date: str) -> str:
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
