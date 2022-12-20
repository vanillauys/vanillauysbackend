# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import typer
from rich import print


# ---------------------------------------------------------------------------- #
# --- Interest Calculator ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def interest(
    initial: float,
    rate: float,
    n: float,
    t: float
):
    total = initial * (1 + ((rate/100) / n))**(n * t)
    return [total, total - initial]


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    initial: float = float(typer.prompt("Initial Value"))
    rate: float = float(typer.prompt("Interest rate in %"))
    n: float = float(typer.prompt("Number of times compounded per year"))
    t: float = float(typer.prompt("Time in years"))
    result = interest(initial, rate, n, t)
    print(f"[green] Total Value[/green]: {round(result[0], 2)}")
    print(f"[green] Interest Received[/green]: {round(result[1], 2)}")


if __name__ == '__main__':
    typer.run(main)
