# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import os
from deta import Deta
from dotenv import load_dotenv
from schemas import Schemas
from auth.auth_manager import Auth
from typing import Dict, Tuple


# ---------------------------------------------------------------------------- #
# --- Budgets Database ------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()

class BudgetsDB():

    auth = Auth()
    schemas = Schemas()
    PROJECT_KEY = os.getenv('DETA_PROJECT_KEY')
    deta = Deta(PROJECT_KEY)
    budgets = deta.Base('budgets')


    def create_budget(self, budget: schemas.CreateBudget) -> Tuple[int, str]:
        code, response, _ = self.check_budgets_by_email_and_title(budget.email, budget.title)

        if code == 200:
            return 409, f"budget with title '{budget.title}' already exists for '{budget.email}'"
        if code == 500:
            return 500, response

        data = {
            'email': budget.email,
            'title': budget.title,
            'income': {},
            'expenses': {}
        }
        try:
            self.budgets.put(data)
            return 200, f"'{budget.title}' successfully created for '{budget.email}'."
        except Exception:
            return 500, f"an error occurred while creating '{budget.title}' for '{budget.email}'."


    def delete_budget(self, key: str) -> Tuple[int, str]:
        try:
            self.budgets.delete(key)
            return 200, f"succesfully deleted budget '{key}' from db."
        except Exception:
            return 500, f"an error occured while trying to delete budget '{key}' from db."


    def update_budget(self, budget: schemas.UpdateBudget) -> Tuple[int, str]:
        updates = {
            'title': budget.title,
            'income': budget.income,
            'expenses': budget.expenses
        }
        try:
            self.budgets.update(updates, budget.key)
            return 200, f"successfully updated budget '{budget.key}' for '{budget.email}'."
        except Exception:
            return 500, f"an error occured while updating budget '{budget.key}' for '{budget.email}."


    def get_all_budgets_by_email(self, email: str) -> Tuple[int, str, list[Dict]]:
        try:
            results = self.budgets.fetch({'email': email})
            budgets = results.items
            return 200, f"successfully found budgets for '{email}'", budgets
        except Exception:
            return 500, f'an error occurred while fetching budgets for {email}.', None


    def get_budget_by_key(self, key: str) -> Tuple[int, str, Dict]:
        try:
            budget = self.budgets.get(key)
            if budget is None:
                return 404, f"no budget with key '{key}' found in db.", None

            return 200, f"successfully found budget with key '{key}'", budget
        except:
            return 500, f"an error occurred while fetching budget with key '{key}'", None


    def check_budgets_by_email_and_title(self, email: str, title: str) -> Tuple[int, str, list[Dict]]:
        try:
            results = self.budgets.fetch({'email': email})
            budgets = results.items
            budgets = [x for x in budgets if x['title'] == title]

            if not budgets:
                return 404, f"no budgets by '{email}' with title '{title}' found in db.", None
 
            return 200, f"found budgets by '{email}' with title '{title}'", budgets

        except Exception:
            return 500, f"an error occurred while fetching budgets for '{email}' with title '{title}'", None
