import datetime


# Date Validation
def validate_date(date, format=None):
    if format is None:
        format = "%m/%y"
    try:
        present = datetime.datetime.today()
        result = datetime.datetime.strptime(date, format)
        if present < result:
            return result
        return False
    except ValueError:
        return False
