from datetime import datetime


def get_datetime_object(datetime_str):
    return datetime.strptime(datetime_str, '%m/%d/%YT%H:%M:%SZ')
