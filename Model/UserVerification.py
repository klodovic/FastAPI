from pydantic import BaseModel, Field
from typing import Optional


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)