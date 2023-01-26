# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from pydantic import BaseModel, Field, EmailStr
from typing import Dict


# ---------------------------------------------------------------------------- #
# --- Schemas Class ---------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Schemas():


    # ------------------------------------------------------------------------ #
    # --- General Schemas ---------------------------------------------------- #
    # ------------------------------------------------------------------------ #


    class DetailClass(BaseModel):
        detail: str = Field(default=None)

    Detail: DetailClass = DetailClass

    def detail(self):
        return self.Detail


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

    def interest_body(self):
        return self.InterestBody

    def interest(self):
        return self.Interest

    def age(self):
        return self.Age


    # ------------------------------------------------------------------------ #
    # --- Crypto Schemas ----------------------------------------------------- #
    # ------------------------------------------------------------------------ #


    class CryptoClass(BaseModel):
        name: str
        price: float
        change: float

    Crypto: CryptoClass = CryptoClass

    def crypto(self):
        return self.Crypto


    # ------------------------------------------------------------------------ #
    # --- User Schemas ------------------------------------------------------- #
    # ------------------------------------------------------------------------ #


    class UserSchemaClass(BaseModel):
        username: str = Field(default=None)
        email: EmailStr = Field(default=None)
        password: str = Field(default=None)

    class UserLoginSchemaClass(BaseModel):
        email: EmailStr = Field(default=None)
        password: str = Field(default=None)

    class LoggedInClass(BaseModel):
        email: EmailStr
        access_token: str
        refresh_token: str

    UserSchema: UserSchemaClass = UserSchemaClass
    UserLoginSchema: UserLoginSchemaClass = UserLoginSchemaClass
    LoggedIn: LoggedInClass = LoggedInClass

    def user_schema(self):
        return self.UserSchema

    def user_login_schema(self):
        return self.UserLoginSchema

    def logged_in(self):
        return self.LoggedIn


    # ------------------------------------------------------------------------ #
    # --- Budget Schemas ----------------------------------------------------- #
    # ------------------------------------------------------------------------ #


    class CreateBudgetClass(BaseModel):
        email: EmailStr
        name: str

    class DeleteBudgetClass(BaseModel):
        email: EmailStr
        key: str

    class UpdateBudgetClass(BaseModel):
        email: EmailStr
        key: str
        income: Dict[str, float,]
        expenses: Dict[str, float]

    CreateBudget: CreateBudgetClass = CreateBudgetClass
    DeleteBudget: DeleteBudgetClass = DeleteBudgetClass
    UpdateBudget: UpdateBudgetClass = UpdateBudgetClass

    def create_budget(self):
        return self.CreateBudget

    def delete_budget(self):
        return self.DeleteBudget

    def update_budget(self):
        return self.UpdateBudget


    # ------------------------------------------------------------------------ #
    # --- Notes Schemas ------------------------------------------------------ #
    # ------------------------------------------------------------------------ #


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

    CreateNote: CreateNoteClass = CreateNoteClass
    UpdateNote: UpdateNoteClass = UpdateNoteClass
    DeleteNote: DeleteNoteClass = DeleteNoteClass

    def create_note(self):
        return self.CreateNote

    def update_note(self):
        return self.UpdateNote

    def delete_note(self):
        return self.DeleteNote
