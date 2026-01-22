from typing import Optional

import pandas as pd


def log_to_file(file_name: str = "../logs/reports.log"):
    def wrapper(function):
        def inner(*args, **kwargs):
            result = function(*args, **kwargs)
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(f"Function '{function.__name__}' was called.\n")
                arguments = [arg for arg in args if not isinstance(arg, pd.DataFrame)]
                f.write(f"Arguments: {arguments}.\n")
                f.write(f"Result:\n{result}\n")
            return result

        return inner

    return wrapper


def spending_by_category(transactions: pd.DataFrame, category: str, end_date: Optional[str] = None) -> pd.DataFrame:
    """Генерирует отчет по тратам в указанной категории за последние три месяца от переданной даты.
    Дата должна быть в формате 'YYYY-MM-DD HH:MM:SS'. Если дата не указана, используется сегодняшняя дата."""
    if end_date:
        end_date = pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
    else:
        end_date = pd.Timestamp.now()

    start_date = end_date - pd.DateOffset(months=3)

    dates = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    mask = (transactions["Категория"] == category) & dates.between(start_date, end_date, inclusive="both")

    result = transactions.loc[mask].copy()

    return result.set_index("Дата операции", drop=True)


@log_to_file()
def spending_by_category_logged(
    transactions: pd.DataFrame, category: str, end_date: Optional[str] = None
) -> pd.DataFrame:
    return spending_by_category(transactions, category, end_date)
