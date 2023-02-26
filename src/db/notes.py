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
    PROJECT_KEY = os.getenv('DETA_KEY')
    deta = Deta(PROJECT_KEY)
    notes = deta.Base('notes')


    def create_note(self, note: schemas.CreateNote) -> Tuple[int, str]:
        data = {
            'email': note.email,
            'title': note.title,
            'body': note.body
        }
        try:
            self.notes.put(data)
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
        updates = {
            'title': note.title,
            'body': note.body
        }
        try:
            self.notes.update(updates, note.key)
            return 200, f"successfully updated note '{note.key}' for '{note.email}'."
        except Exception:
            return 500, f"an error occured while updating note '{note.key}' for '{note.email}."


    def get_all_notes_by_email(self, email: str) -> Tuple[int, str, list[Dict]]:
        try:
            results = self.notes.fetch({'email': email})
            notes = results.items
            return 200, f"successfully found notes for '{email}'", notes
        except Exception:
            return 500, f"an error occurred while fetching notes for '{email}'.", None


    def get_note_by_key(self, key: str) -> Tuple[int, str, Dict]:
        try:
            note = self.notes.get(key)
            if note is None:
                return 404, f"no note with key '{key}' found in db.", None

            return 200, f"successfully found note with key '{key}'", note
        except:
            return 500, f"an error occurred while fetching note with key '{key}'", None
