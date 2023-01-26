# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from typing import Dict, Tuple


# ---------------------------------------------------------------------------- #
# --- Interest Calculator ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class InterestCalculator():


    def interest(
        self,
        initial: float,
        rate: float,
        n: float,
        t: float
    ) -> Tuple[int, str, Dict[float, float]]:
        if type(initial) != float:
            return 400, 'Initial needs to be a number.', None
        if initial <= 0:
            return 400, 'Initial value must be positive.', None
        if type(rate) != float:
            return 400, 'Rate needs to be a number.', None
        if rate <= 0:
            return 400, 'Rate must be positive.', None
        if type(n) != float:
            return 400, 'Time needs to be a number.', None
        if n <= 0:
            return 400, 'Time must be positive.', None

        total = initial * (1 + ((rate/100) / n))**(n * t)
        result = {
            'total': total,
            'interest': total - initial
        }
        return 200, 'successfully calculated the total value and interest received', result


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    # Nothing to do here
    pass


if __name__ == '__main__':
    main()
