from pydantic import BaseModel


class SignInModel(BaseModel):
    email: str
    password: str

class SignUpModel(BaseModel):
    name: str
    email: str
    password: str