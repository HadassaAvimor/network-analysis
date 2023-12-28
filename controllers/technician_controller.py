import controllers.authn_authz
from models.technician import Technician
from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm
from controllers.authn_authz import Token, get_current_technician

technicians_router = APIRouter()


@technicians_router.post('/login', response_model=Token)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    return await controllers.authn_authz.login_for_access_token(response, form_data)


@technicians_router.get('/me', summary='Get details of currently logged in user')
async def get_me(technician: Technician = Depends(get_current_technician)):
    return technician
