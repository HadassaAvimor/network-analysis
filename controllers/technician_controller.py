from fastapi import Response, status, APIRouter
from models.technician import Technician

technicians_router = APIRouter()
technicians = [
    {
        "name": "Technician 1",
        "id": 1,
        "email": "technician1@example.com",
        "phone_number": "123-456-7890",
        "skills": ["technicianing", "sysadmin", "security"],
    },
    {
        "name": "Technician 2",
        "id": 2,
        "email": "technician2@example.com",
        "phone_number": "555-678-9012",
        "skills": ["programming", "databases", "cloud computing"],
    },
]


@technicians_router.get("/", status_code=status.HTTP_200_OK)
async def get_technicians():
    return technicians


@technicians_router.get("/id/{technician_id}", status_code=status.HTTP_200_OK)
async def get_technician_by_id(technician_id):
    return [technician for technician in technicians if technician['id'] == int(technician_id)][0]


@technicians_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_technician(technician: Technician):
    name = technician.name
    id = technician.id
    hash_password = technician.hash_password

    technician = {
        "name": name,
        "id": id,
        "hash_password": hash_password
    }

    technicians.append(technician)
    return technician


@technicians_router.put("/id/{technician_id}", status_code=status.HTTP_200_OK)
async def update_technician(technician_id: int, technician: Technician):
    technician_update = technicians[technician_id - 1]
    technician_update.name = technician.name
    technician_update.hash_password = technician.hash_password

    return technician_update


@technicians_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_technician(technician_id: int):
    technicians.pop(technician_id - 1)
    return
