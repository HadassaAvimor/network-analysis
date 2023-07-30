from typing import Optional
from pydantic import BaseModel


class Technician(BaseModel):
    id: int
    name: str
    hash_password: str
    permission: Optional[list] = None
    clients: Optional[list] = None
