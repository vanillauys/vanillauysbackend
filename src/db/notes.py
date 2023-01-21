# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from db.db_conf import notes


# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


def create_note(email: str, title: str, body: str):
    status, note = check_notes(email, title)

    if not status:
        return False, f'an error occured while creating {title}.'

    if note:
        return False, f'the note {title} already exists in the db.'

    note = {
        'email': email,
        'title': title,
        'body': body
    }
    try:
        notes.put(note)
        return True, f'{title} created successully.'
    except Exception:
        return False, f'an error occurred while creating {title}.'


def check_notes(email: str, title: str):
    try:
        results = notes.fetch({'email': email})
        note = results.items
        note = [x for x in note if x['title'] == title]
        return True, note
    except Exception:
        return False, None


def delete_note(key: str):
    try:
        notes.delete(key)
        return True, f'succesfully deleted {key} from db.'
    except Exception:
        return False, f'an error occured while trying to delete {key} from db.'


def update_note(key: str, title: str, body: str):
    updates = {
        'title': title,
        'body': body
    }
    try:
        notes.update(updates, key)
        return True, 'successfully updated the note in db.'
    except Exception:
        return False, 'an error occurred while updating the note.'


def get_all_notes(email: str):
    try:
        results = notes.fetch({'email': email})
        note = results.items
        return True, note
    except Exception:
        return False, f'an error occurred while fetching notes for {email}.'


def get_note(key: str):
    try:
        result = notes.get(key)
        if result is None:
            return False, f'no note with key {key} found in db.'

        del result['email']
        return True, result
    except:
        return False, f'an error occurred while getting note with key {key}'
