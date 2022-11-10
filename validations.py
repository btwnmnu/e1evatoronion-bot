import datetime
import re

def checkDate(date):
    min_date = datetime.date(2022, 1, 1)
    max_date = (datetime.datetime.now() + datetime.timedelta(hours=3)).date()

    if len(date.split('.')) == 3:
        try:
            datetime.datetime.strptime(date, "%d.%m.%Y").date()
            pattern = '\d\d\.\d\d\.\d\d\d\d'
            if re.match(pattern, date):
                result = True
            else:
                result = False        
        except Exception:
            result = False
    else:
        result = False

    if result and ((datetime.datetime.strptime(date, "%d.%m.%Y").date()) < min_date):
        return('old')
    elif result and ((datetime.datetime.strptime(date, "%d.%m.%Y").date()) > max_date):
        return('future')
    elif not result:
        return('error')
    else:
        return('good')

