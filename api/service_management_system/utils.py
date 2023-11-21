from datetime import datetime, timedelta


def get_utc_date(days=0, hours=0, minutes=0, seconds=0):
    session_date = datetime.now()
    session_date += timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return session_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
