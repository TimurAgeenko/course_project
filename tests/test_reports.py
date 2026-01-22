from src.reports import spending_by_category, log_to_file
import pandas as pd
import os


def test_spending_by_category():
    data = pd.read_excel("./data/operations.xlsx")
    category = "Супермаркеты"
    end_date = "2021-09-15 00:00:00"
    report = spending_by_category(data, category, end_date)
    assert report["Категория"].nunique() == 1
    assert pd.to_datetime(report.index.min(), format="%d.%m.%Y %H:%M:%S") >= pd.to_datetime(
        "2021-06-15 00:00:00", format="%Y-%m-%d %H:%M:%S"
    )
    assert pd.to_datetime(report.index.max(), format="%d.%m.%Y %H:%M:%S") <= pd.to_datetime(
        "2021-09-15 00:00:00", format="%Y-%m-%d %H:%M:%S"
    )


def test_spending_by_category_no_end_date():
    data = pd.read_excel("./data/operations.xlsx")
    category = "Супермаркеты"
    report = spending_by_category(data, category)
    assert report.empty


def test_log_to_file():
    @log_to_file("./logs/test_log.log")
    def add(a, b):
        return a + b

    add(1, 2)

    with open("./logs/test_log.log", "r", encoding="utf-8") as f:
        log_content = f.read()

    assert log_content == "Function 'add' was called.\nArguments: [1, 2].\nResult:\n3\n"

    os.remove("./logs/test_log.log")
