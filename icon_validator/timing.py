from datetime import datetime


def time_now():
    return datetime.utcnow()


def format_time(start, end):
    """
    Returns the time delta of two datetimes in a millisecond floating point number.
    :param start: Start datetime
    :param end: End dtaetime
    :return: the milliseconds between start and end, as a floating point number
    """
    return (end - start).total_seconds() * 1000
