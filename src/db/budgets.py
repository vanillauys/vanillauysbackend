# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from db_conf import budgets


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
        return False, f'an error occurred while creating {budget_name}.'


def delete_budget(email: str, budget_name: str):
    status, budget = check_budget(email, budget_name)
    if not status:
        return False, f'an error occured while trying to delete {budget_name} from db.'
    
    if not budget:
        return False, f'{budget_name} does not exist in db.'

    key = budget[0]['key']
    try:
        budgets.delete(key)
        return True, f'succesfully deleted {budget_name} from db.'
    except Exception:
        return False, f'an error occured while trying to delete {budget_name} from db.'


def check_budget(email: str, budget_name: str):
    try:
        results = budgets.fetch({'email': email}, {'name': budget_name})
        budget = results.items
        return True, budget
    except Exception:
        return False, None
