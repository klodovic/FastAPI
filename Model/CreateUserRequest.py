from pydantic import BaseModel, Field
from typing import Optional


class CreateUserRequest(BaseModel):
    user_name: str
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    role: str

    class Config:
        json_schema_extra = {
            'example':{
                'user_name': 'doc',
                'email': 'd@d.hr',
                'first_name': 'Doktor',
                'last_name': 'Doktorovic',
                'hashed_password': '',
                'role': 'user',
            }
        }


