import datetime


# Date Validation
def validate_date(date, formats=None):
    if formats is None:
        formats = ["%m/%y", "%m/%Y"]
    for f in formats:
        try:
            present = datetime.datetime.today()
            result = datetime.datetime.strptime(date, f)
            if present < result:
                return True, result
            return False, "This date is in the past."
        except ValueError:
            pass
    return False, "Incorrect format, should read: 'mm/yy' or 'mm/yyyy'"
