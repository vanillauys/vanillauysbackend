# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from db.db_conf import budgets


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def create_budget(email: str, budget_name: str):
    status, budget = check_budget(email, budget_name)

    if not status:
        return False, f'an error occured while creating {budget_name}.'

    if budget:
        return False, f'{budget_name} already exists in the db.'

    budget = {
        'email': email,
        'name': budget_name,
        'income': {},
        'expenses': {}
    }
    try:
        budgets.put(budget)
        return True, f'{budget_name} created successully.'
    except Exception:
        return False, f'an 2 error occurred while creating {budget_name}.'


def delete_budget(key: str):
    try:
        budgets.delete(key)
        return True, f'succesfully deleted {key} from db.'
    except Exception:
        return False, f'an error occured while trying to delete {key} from db.'


def check_budget(email: str, budget_name: str):
    try:
        results = budgets.fetch({'email': email})
        budget = results.items
        budget = [x for x in budget if x['name'] == budget_name]
        return True, budget
    except Exception:
        return False, None


def update_budget(key: str, income: dict, expenses: dict):
    updates = {
        'income': income,
        'expenses': expenses
    }
    try:
        budgets.update(updates, key)
        return True, 'successfully updated the budget in db.'
    except Exception:
        return False, 'an error occurred while updating the budget.'


def get_all_budgets(email: str):
    try:
        results = budgets.fetch({'email': email})
        budget = results.items
        return True, budget
    except Exception:
        return False, f'an error occurred while fetching budgets for {email}.'


def get_budget(key: str):
    try:
        result = budgets.get(key)
        if result is None:
            return False, f'no budget with key {key} found in db.'
        
        return True, result
    except:
        return False, f'an error occurred while getting budget with key {key}'
