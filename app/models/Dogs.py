from sqlmodel import Field, SQLModel


class Dogs(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    breed: str
    age: int
    owner: str 
