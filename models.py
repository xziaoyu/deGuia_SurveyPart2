from sqlmodel import Field , SQLModel

class Surveynimo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: str
    place_of_birth: str
    favorite_food: str
    are_you_gay: str
    hobby1: str
    hobby2: str
    hobby3: str
    Current_school: str
    Useless_skill: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    userr: str
    passwordd: str
       