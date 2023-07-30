import os
from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import ValidationError, BaseModel
from starlette import status
from jose import JWTError, jwt

from models.DB_connection import insert_row
from models.technician import TechnicianInDB, Technician

ACCESS_TOKEN_EXPIRE_MINUTES = 30
# REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']


# JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(Token):
    username: Union[str, None] = None


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def get_current_technician(token: str = Depends(reusable_oauth)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = db.get(token_data.sub, None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find technician",
        )

    return TechnicianInDB(**user)


async def create_technician(technician: Technician) -> Technician:
    """
    Creates a new technician in the database.

    Args:
        technician: The technician to create.

    Returns:
        The created technician.
    """

    # Check if the technician already exists.
    # user = Technician.query.filter_by(user_name=technician.user_name).first()
    # if user is not None:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="technician with this name already exist"
    #     )

    hashed_password = get_hashed_password(technician.password)
    access_token = create_access_token(technician.name)
    # refresh_token = create_refresh_token(user['user_name'])

    insert_row("Technicians", {'Username': technician.name, 'Password': hashed_password})
    return technician


def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Logs in a technician.

    Args:
        form_data: The form data from the login request.

    Returns:
        The access token and refresh token for the logged-in technician.
    """

    # Get the technician from the database.
    #TODO fix it to the right function of selsct from db
    user = Technician.query.filter_by(user_name=form_data.username).first()

    # Check if the username and password are correct.
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    # Create the access token and refresh token.
    access_token = create_access_token(user['user_name'])
    # refresh_token = create_refresh_token(user['user_name'])

    return {
        "access_token": access_token,
        # "refresh_token": refresh_token,
    }

# def create_refresh_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
#     else:
#         expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
#
#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
#     return encoded_jwt
