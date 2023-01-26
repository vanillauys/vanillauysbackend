# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from datetime import datetime
from dateutil import relativedelta
from typing import Dict, Tuple


# ---------------------------------------------------------------------------- #
# --- Calculator ------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class DateCalculator():


    def calculate_time(self, start_date: str, end_date: str) -> Tuple[int, str, Dict]:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except Exception:
            return 400, "The format of start or end date is invalid.", None

        if end < start:
            print('End date cannot be before start date.')
            return 400, "The end date cannot be before start date.", None

        delta = relativedelta.relativedelta(end, start)
        if delta.years > 285616413:
            return 400, "Maximum time delta exceeded. (285616413 years)", None

        seconds = (end - start).total_seconds()
        minutes = seconds / 60
        hours = seconds / 3600
        days = (end - start).days
        weeks = [(days - (days % 7)) / 7, days % 7]
        md = [(delta.years * 12) + delta.months, delta.days]
        ymd = [delta.years, delta.months, delta.days]

        time = {
            'seconds': seconds,
            'minutes': minutes,
            'hours': hours,
            'days': days,
            'weeks': weeks,
            'md': md,
            'ymd': ymd
        }
        return 200, f"succesfully calculated the time between '{start_date}' and '{end_date}'", time 


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    # Nothing to do here
    pass


if __name__ == '__main__':
    main()
