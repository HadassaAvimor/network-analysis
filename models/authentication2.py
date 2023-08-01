import os
from datetime import datetime, timedelta
from typing import Union, Optional, Dict
from jose import jwt, JWTError
from fastapi import Depends, FastAPI, HTTPException, status, Request, Response, encoders
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, \
    OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from passlib.context import CryptContext
from models.technician import Technician, TechnicianInDB
from starlette.status import HTTP_401_UNAUTHORIZED
from dotenv import load_dotenv
from models.insert_to_db import insert_to_technician
load_dotenv()
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "name": "johndoe",
        "hashed_password": "$2b$12$UEWlwXzDke9OUeHefcPm.eBTSgskCESsHXsNvx3c8RrvWftxQRoAe",
    }
}


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("Authorization")  # changed to accept access token from httpOnly Cookie

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    technician_name: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_cookie_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# TODO: ליצור קשר עם דיבי ולא לקבל כפרמטר
def get_technician(db, technician_name: str):
    if technician_name in db:
        technician_dict = db[technician_name]
        print(technician_dict)
        return TechnicianInDB(**technician_dict)


def authenticate_technician(fake_db, technician_name: str, password: str):
    technician: Technician = get_technician(fake_db, technician_name)
    if not technician:
        return None
    if not verify_password(password, technician.hashed_password):
        return None
    return technician


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_technician(token: str = Depends(oauth2_cookie_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        technician_name: str = payload.get("sub")
        if technician_name is None:
            raise credentials_exception
        token_data = TokenData(technician_name=technician_name)
    except JWTError:
        raise credentials_exception
    technician = get_technician(fake_users_db, technician_name=token_data.technician_name)
    if technician is None:
        raise credentials_exception
    return technician


async def get_current_active_technician(current_technician: Technician = Depends(get_current_technician)):
    # if current_technician and current_technician.disabled:
    # raise HTTPException(status_code=400, detail="Inactive user")
    return current_technician


async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    technician = authenticate_technician(fake_users_db, form_data.username, form_data.password)
    if not technician:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": technician.name}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def create_technician(response, technician: Technician) -> dict[str, Technician | str]:
    """
    Creates a new technician in the database.

    Args:
        technician: The technician to create.

    Returns:
        The created technician.
    """

    # Check if the technician already exists.
    user = Technician.query.filter_by(user_name=technician.name).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="technician with this name already exist"
        )

    hashed_password = get_password_hash(technician.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": technician.name}, expires_delta=access_token_expires)
    insert_to_technician({'Username': technician.name, 'Password': hashed_password})
    response.set_cookie(
        key="Authorization", value=f"Bearer {encoders.jsonable_encoder(access_token)}",
        httponly=True
    )
    return {'technician': technician, 'token': access_token, }