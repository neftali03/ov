import re
import secrets
import string
from datetime import date, timedelta
from decimal import ROUND_DOWN, Decimal, getcontext
from typing import Any, Literal, Union

import pandas as pd
import unidecode
from num2words import num2words


def clean_spaces(content: str) -> str:
    """Remove multiple spaces from a string."""
    return " ".join(content.split())


def clean_accents(content: str) -> str:
    """Remove multiple spaces from a string."""
    return unidecode.unidecode(content)


def clean_string(content: str) -> str:
    """Remove multiple spaces from a string."""
    content = clean_spaces(content)
    content = clean_accents(content)
    return content


def match_regex(content: str, regex: str) -> bool:
    """Return True if the content matches the regex."""
    return bool(re.compile(regex).match(content))


def pprint_df(df: pd.DataFrame) -> None:
    """Pretty print a dataframe for debugging only."""
    pd.set_option(
        "display.max_rows",
        None,
        "display.max_columns",
        None,
        "display.expand_frame_repr",
        False,
    )
    print(df)  # noqa: T201


def month_delta(value: date, *, months: int) -> date:
    """Return a date plus/minus the given months."""
    month, year = value.month, value.year
    if months < 0:
        for _ in range(abs(months)):
            if month == 1:
                year -= 1
                month = 12
            else:
                month -= 1
    elif months > 0:
        for _ in range(months):
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
    else:
        return value

    extra_days = 0
    while True:
        try:
            return value.replace(year=year, month=month, day=value.day - extra_days)
        except ValueError:
            extra_days += 1


def to_int(value: Any) -> int:
    """Convert a value to an integer, in a best-effort fashion."""
    if type(value) is int:
        return value
    if type(value) is str:
        value = value.replace(",", "")
    return int(value)


def format_docs(number: str, category: Literal["NIT", "DUI", "NRC"]) -> str:
    """Return a properly formatted document number."""
    if number:
        if category == "NIT" and len(number) == 14:
            return f"{number[:4]}-{number[4:10]}-{number[10:13]}-{number[13:]}"
        elif category == "NIT" and len(number) == 9:
            return f"{number[:-1]}-{number[-1:]}"
        elif category in ["DUI", "NRC"]:
            return f"{number[:-1]}-{number[-1:]}"
    return number


def money_as_letter(value: Decimal, currency: str = "") -> str:
    """Return a money amount as letters."""
    getcontext().rounding = ROUND_DOWN
    int_value = value.quantize(Decimal("0"))
    dec_value = int((value - int_value) * 100)
    int_portion = num2words(int_value, lang="es")
    dec_portion = f"con {dec_value}/100" if dec_value else "exactos"
    currency = f" {currency}"
    return clean_accents(f"{int_portion} {dec_portion}{currency}".upper())


NumericType = Union[int, float, Decimal]


def safe_div(numerator: NumericType, denominator: NumericType) -> NumericType:
    """Return the division of two numbers, or zero on error."""
    try:
        return numerator / denominator  # type: ignore[operator]
    except (ZeroDivisionError, TypeError):
        return 0


def yearly_offsets(
    *,
    start: date,
    end: date,
    years: int,
    shift_weekday=False,
) -> list[tuple[date, date]]:
    """Return the given interval offset by 52-weeks years."""
    intervals = []
    for year in range(years + 1):
        interval_start = month_delta(start, months=-12 * year)
        interval_end = month_delta(end, months=-12 * year)
        if shift_weekday:
            days_delta_1 = start.isoweekday() - interval_start.isoweekday()
            opposite_sign = -safe_div(days_delta_1, abs(days_delta_1))
            days_delta_2 = days_delta_1 + 7 * opposite_sign
            if abs(days_delta_1) < abs(days_delta_2):  # type: ignore[operator]
                days_delta = timedelta(days_delta_1)
            else:
                days_delta = timedelta(days_delta_2)  # type: ignore[arg-type]
            interval_start += days_delta
            interval_end += days_delta
        intervals.append((interval_start, interval_end))
    return intervals


def make_random_password(lenght=8) -> str:
    """Return an alphanumeric password."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(lenght))
