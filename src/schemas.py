# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from pydantic import BaseModel, Field, EmailStr
from typing import Dict


# ---------------------------------------------------------------------------- #
# --- General Schemas -------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Message(BaseModel):
    message: str


# ---------------------------------------------------------------------------- #
# --- Caclulators Schemas ---------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Interest(BaseModel):
    total: float
    interest: float


class Age(BaseModel):
    seconds: float
    minutes: float
    hours: float
    days: float
    weeks: list[float]
    md: list[float]
    ymd: list[float]


# ---------------------------------------------------------------------------- #
# --- Crypto Schemas --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Crypto(BaseModel):
    name: str
    price: float
    change: float


# ---------------------------------------------------------------------------- #
# --- User Schemas ----------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class UserSchema(BaseModel):
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)


class LoggedIn(BaseModel):
    email: EmailStr
    access_token: str
    refresh_token: str


# ---------------------------------------------------------------------------- #
# --- Budget Schemas --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class CreateBudget(BaseModel):
    email: EmailStr
    name: str


class DeleteBudget(BaseModel):
    email: EmailStr
    key: str


class UpdateBudget(BaseModel):
    email: EmailStr
    key: str
    income: Dict[str, float,]
    expenses: Dict[str, float]


# ---------------------------------------------------------------------------- #
# --- Notes Schemas ---------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class CreateNote(BaseModel):
    email: EmailStr
    title: str
    body: str


class UpdateNote(BaseModel):
    email: EmailStr
    key: str
    title: str
    body: str


class DeleteNote(BaseModel):
    email: EmailStr
    key: str
