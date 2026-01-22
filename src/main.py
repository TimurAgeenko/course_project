import pandas as pd

from src.reports import spending_by_category_logged
from src.services import get_top_cashback_categories
from src.utils import get_data
from src.views import main_views


def main(date: str, category: str) -> None:
    """Главная функция приложения, которая вызывает функции из других модулей."""
    data = get_data()
    df = pd.read_excel("../data/operations.xlsx")

    print("=== Главная страница ===")
    main_page = main_views(date)
    print(main_page)

    print("\n=== Топ категории по кэшбэку ===")
    cashback_categories = get_top_cashback_categories(
        data=data,
        year=int(date[:4]),
        month=int(date[5:7]),
    )
    print(cashback_categories)

    print("\n=== Отчет по тратам в категории ===")
    report = spending_by_category_logged(df, category, date)
    print(report)
