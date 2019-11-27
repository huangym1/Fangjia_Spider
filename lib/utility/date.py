import time

def get_date_string():
    current = time.localtime()
    return time.strftime("%Y%m%d", current)