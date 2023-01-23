# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from datetime import datetime, date
from dateutil import relativedelta
import typer
from rich import print
from rich.table import Table
from rich.console import Console


# ---------------------------------------------------------------------------- #
# --- Calculator ------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def calculate_time(start_date: str, end_date: str):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except Exception as e:
        print(
            '[bold red]Invalid start or end date[/bold red], please use the correct format.')
        return False, "The format of start or end date is invalid."

    if end < start:
        print('End date cannot be before start date.')
        return False, "The end date cannot be before start date."

    delta = relativedelta.relativedelta(end, start)
    if delta.years > 285616413:
        return False, "Maximum time delta exceeded. (285616413 years)"

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
    return True, time


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    console = Console()
    start_date: str = typer.prompt("Start Date (yyyy-mm-dd)")
    end_date: str = typer.prompt("End Date (yyyy-mm-dd)")
    status, times = calculate_time(start_date, end_date)
    if status:
        table = Table('Time unit', 'Value')
        table.add_row('Seconds', str(round(times['seconds'])))
        table.add_row('Minutes', str(round(times['minutes'])))
        table.add_row('Hours', str(round(times['hours'])))
        table.add_row('Days', str(times['days']))
        table.add_row(
            'Weeks and Days', f"{str(round(times['weeks'][0]))}, {str(round(times['weeks'][1]))}")
        table.add_row(
            'Months and Days', f"{str(round(times['md'][0]))}, {str(round(times['md'][1]))}")
        table.add_row('Years, Months and Days',
                      f"{str(round(times['ymd'][0]))}, {str(round(times['ymd'][1]))}, {str(round(times['ymd'][2]))}")
        console.print(table)
    else:
        print(times)


if __name__ == '__main__':
    typer.run(main)
