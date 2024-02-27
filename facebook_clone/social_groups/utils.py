from django.contrib.humanize.templatetags.humanize import naturalday
from datetime import datetime


def calculate_timestamp(timestamp):
    #print(datetime.now())
    """
    1. Today or yesterday:
        - EX: 'today at 10:56 AM'
        - EX: 'yesterday at 5:19 PM'
    2. other:
        - EX: 05/06/2020
        - EX: 12/12/2020
    """
    #today or yesterday
    if((naturalday(timestamp) == "today") or (naturalday(timestamp) == "yesterday")):
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        ts = f"{naturalday(timestamp)} at {str_time}"
    #other day
    else:
        str_time = datetime.strftime(timestamp, "%m/%d/%Y")
        ts = f"{str_time}"
    return str(ts)