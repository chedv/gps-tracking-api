from datetime import datetime
import pytz


def utc_datetime(str_datetime):
    utc_object = datetime.strptime(str_datetime, '%m/%d/%Y %H:%M:%S')
    return utc_object.replace(tzinfo=pytz.UTC)
