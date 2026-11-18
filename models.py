from pydantic import BaseModel, Field as FormField
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    username_hash: str = Field(primary_key=True)
    password_hash: str


class LoginForm(BaseModel):
    username: str = FormField(min_length=1, max_length=80)
    password: str = FormField(min_length=1, max_length=128)


class RegisterForm(LoginForm):
    confirm_password: str = FormField(min_length=1, max_length=128)