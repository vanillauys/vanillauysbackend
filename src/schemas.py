# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from pydantic import BaseModel, EmailStr
from typing import Dict


# ---------------------------------------------------------------------------- #
# --- Schemas Class ---------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Schemas():


    # ------------------------------------------------------------------------ #
    # --- General Schemas ---------------------------------------------------- #
    # ------------------------------------------------------------------------ #


    class DetailClass(BaseModel):
        detail: str

    Detail: DetailClass = DetailClass


    # ------------------------------------------------------------------------ #
    # --- Caclulators Schemas ------------------------------------------------ #
    # ------------------------------------------------------------------------ #


    class InterestBodyClass(BaseModel):
        initial: float
        rate: float
        n: float
        t: float

    class InterestClass(BaseModel):
        total: float
        interest: float

    class AgeClass(BaseModel):
        seconds: float
        minutes: float
        hours: float
        days: float
        weeks: list[float]
        md: list[float]
        ymd: list[float]

    InterestBody: InterestBodyClass = InterestBodyClass
    Interest: InterestClass = InterestClass
    Age: AgeClass = AgeClass


    # ------------------------------------------------------------------------ #
    # --- Crypto Schemas ----------------------------------------------------- #
    # ------------------------------------------------------------------------ #


    class CryptoClass(BaseModel):
        name: str
        price: float
        change: float

    Crypto: CryptoClass = CryptoClass


    # ------------------------------------------------------------------------ #
    # --- User Schemas ------------------------------------------------------- #
    # ------------------------------------------------------------------------ #


    class UserSchemaClass(BaseModel):
        username: str
        email: EmailStr
        password: str

    class UserLoginSchemaClass(BaseModel):
        email: EmailStr
        password: str

    class LoggedInClass(BaseModel):
        email: EmailStr
        access_token: str
        refresh_token: str

    UserSchema: UserSchemaClass = UserSchemaClass
    UserLoginSchema: UserLoginSchemaClass = UserLoginSchemaClass
    LoggedIn: LoggedInClass = LoggedInClass


    # ------------------------------------------------------------------------ #
    # --- Budget Schemas ----------------------------------------------------- #
    # ------------------------------------------------------------------------ #

    class BudgetClass(BaseModel):
        key: str
        email: EmailStr
        income: dict
        expenses: dict

    class CreateBudgetClass(BaseModel):
        email: EmailStr
        name: str

    class DeleteBudgetClass(BaseModel):
        email: EmailStr
        key: str

    class UpdateBudgetClass(BaseModel):
        email: EmailStr
        key: str
        income: Dict[str, float]
        expenses: Dict[str, float]

    Budget: BudgetClass = BudgetClass
    CreateBudget: CreateBudgetClass = CreateBudgetClass
    DeleteBudget: DeleteBudgetClass = DeleteBudgetClass
    UpdateBudget: UpdateBudgetClass = UpdateBudgetClass


    # ------------------------------------------------------------------------ #
    # --- Notes Schemas ------------------------------------------------------ #
    # ------------------------------------------------------------------------ #

    class NotesClass(BaseModel):
        key: str
        email: EmailStr
        title: str
        body: str

    class CreateNoteClass(BaseModel):
        email: EmailStr
        title: str
        body: str

    class UpdateNoteClass(BaseModel):
        email: EmailStr
        key: str
        title: str
        body: str

    class DeleteNoteClass(BaseModel):
        email: EmailStr
        key: str

    Notes: NotesClass = NotesClass
    CreateNote: CreateNoteClass = CreateNoteClass
    UpdateNote: UpdateNoteClass = UpdateNoteClass
    DeleteNote: DeleteNoteClass = DeleteNoteClass
