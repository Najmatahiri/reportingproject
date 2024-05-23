from datetime import datetime


def month_year(date=datetime.today().strftime('%d-%m-%Y')):
    current_date__month = date.split('-')[1]
    current_date__year = date.split('-')[2].lstrip('0')
    return current_date__month, current_date__year
