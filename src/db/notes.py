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
# --- Notes Database --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()

class NotesDB():

    auth = Auth()
    schemas = Schemas()
    PROJECT_KEY = os.getenv('DETA_PROJECT_KEY')
    deta = Deta(PROJECT_KEY)
    notes = deta.Base('notes')


    def create_note(self, note: schemas.CreateNote) -> Tuple[int, str]:
        note.email = str(note.email)
        code, response, _ = self.check_notes_by_email_and_title(note.email, note.title)

        if code == 200:
            return 409, f"note with title '{note.title} already exists for '{note.email}'"
        if code == 500:
            return 500, response

        note = {
            'email': note.email,
            'title': note.title,
            'body': note.body
        }
        try:
            self.notes.put(note)
            return 200, f"'{note.title}' successfully created for '{note.email}'."
        except Exception:
            return 500, f"an error occurred while creating '{note.title}' for '{note.email}'."


    def delete_note(self, key: str) -> Tuple[int, str]:
        try:
            self.notes.delete(key)
            return 200, f"succesfully deleted note '{key}' from db."
        except Exception:
            return 500, f"an error occured while trying to delete note '{key}' from db."


    def update_note(self, note: schemas.UpdateNote) -> Tuple[int, str]:
        note.email = str(note.email)
        updates = {
            'title': note.title,
            'body': note.body
        }
        try:
            self.notes.update(updates, note.key)
            return 200, f"successfully updated note '{note.key}' for '{note.email}'."
        except Exception:
            return 500, f"an error occured while updating note '{note.key}' for '{note.email}."


    def check_notes_by_email_and_title(self, email: str, title: str) -> Tuple[int, str, list[Dict]]:
        try:
            results = self.notes.fetch({'email': email})
            notes = results.items
            notes = [x for x in notes if x['title'] == title]

            if not notes:
                return 404, f"no notes by '{email}' with title '{title}' found in db.", None
 
            return 200, f"found notes by '{email}' with title '{title}'", notes

        except Exception:
            return 500, f"an error occurred while fetching notes for '{email}' with title '{title}'", None


    def get_all_notes_by_email(self, email: str) -> Tuple[int, str, list[Dict]]:
        try:
            results = self.notes.fetch({'email': email})
            notes = results.items
            return 200, f"successfully found notes for '{email}'", notes
        except Exception:
            return 500, f'an error occurred while fetching notes for {email}.', None


    def get_note_by_key(self, key: str) -> Tuple[int, str, Dict]:
        try:
            note = self.notes.get(key)
            if note is None:
                return 404, f"no note with key '{key}' found in db.", None

            return 200, f"successfully found note with key '{key}'", note
        except:
            return 500, f"an error occurred while fetching note with key '{key}'", None
