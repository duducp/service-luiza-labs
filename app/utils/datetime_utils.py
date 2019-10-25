from datetime import datetime

import dateutil.parser
import pytz


def get_datetime(timezone: str = "America/Sao_Paulo") -> datetime:
    """
    Captures the datetime of a given timezone
    """
    return datetime.now(tz=pytz.timezone(timezone))


def convert_to_timezone(
    date, timezone: str = "UTC", timezone_date: str = "UTC"
) -> datetime:
    """
    Converts a date to a given timezone
    :param date: Date for conversion
    :param timezone: Timezone to be converted
    :param timezone_date: Timezone name of the entered date.
    :return: datetime
    """
    if not isinstance(date, datetime):
        date = dateutil.parser.parse(date)

    if date.tzinfo is None:
        date = pytz.timezone(timezone_date).localize(date, is_dst=False)

    timezone = pytz.timezone(timezone)
    date = date.astimezone(timezone)
    return date
