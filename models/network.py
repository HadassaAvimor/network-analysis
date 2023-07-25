import time
from typing import Tuple
from pydantic import BaseModel
from technician import Technician


class Network(BaseModel):
    id: int
    name: str
    date: time.time()
    client_id: int
    technician: Technician
    location: str
    devices: list
    connections: list[Tuple]



