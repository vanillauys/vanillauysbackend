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
