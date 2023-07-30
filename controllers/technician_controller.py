from fastapi.security import OAuth2PasswordRequestForm

import models.authentication
from models.technician import Technician
from fastapi import status, APIRouter, Depends
from models.authentication import get_current_technician
technicians_router = APIRouter()


# @technicians_router.get("/", status_code=status.HTTP_200_OK)
# async def get_technicians():
#     return 'jh'
#
#
# @technicians_router.get("/id/{technician_id}", status_code=status.HTTP_200_OK)
# async def get_technician_by_id(technician_id):
#     return [technician for technician in technicians if technician['id'] == int(technician_id)][0]


@technicians_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_technician(technician: Technician) -> Technician:
    return await models.authentication.create_technician(technician)


@technicians_router.post('/login', )
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    return await login(form_data)


@technicians_router.get('/me', summary='Get details of currently logged in user')
async def get_me(technician: Technician = Depends(get_current_technician)):
    return technician
