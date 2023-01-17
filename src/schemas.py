# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from pydantic import BaseModel, Field, EmailStr
from typing import Union
from datetime import datetime


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
    access_token: str
    refresh_token: str
