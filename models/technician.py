from typing import Optional
from pydantic import BaseModel


class Technician(BaseModel):
    # id: int
    password: str
    name: str
    permission: Optional[list] = None
    clients: Optional[list] = None


class TechnicianInDB(Technician):
    hashed_password: str




