from typing import Optional
from pydantic import BaseModel


class Technician(BaseModel):
    name: str
    password: str
    clients_permission: Optional[list[dict]] = None
    clients: Optional[list] = None




