from typing import Optional
from pydantic import BaseModel


class Technician(BaseModel):
    name: str
    password: str
    clients_id_permission: Optional[list] = None
    clients: Optional[list] = None




