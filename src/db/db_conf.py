# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from dotenv import load_dotenv
from deta import Deta
import os


# ---------------------------------------------------------------------------- #
# --- Configuration ---------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()
PROJECT_KEY = os.environ.get('DETA_PROJECT_KEY')
deta = Deta(PROJECT_KEY)
users = deta.Base('users')
budgets = deta.Base('budgets')


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def main():
    # Nothing to do here
    pass


if __name__ == '__main__':
    main()
