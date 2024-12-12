import fastapi

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import exceptions.users
import operations.users
import responses.users
from operations.users import get_new_access_token

users_router = fastapi.APIRouter()


@users_router.post('/sign-in', response_model=responses.users.Authentication)
def sign_in(request: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()]):
    try:
        access_token, refresh_token = operations.users.sign_in(request.username, request.password)

        response = JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "Bearer"
            }
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=7 * 24 * 60 * 60
        )

        return response

    except exceptions.users.UserDoesNotExistException:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="User does not exist",
        )
    except exceptions.users.WrongCredentialsException:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
        )

@users_router.post("/refresh-token", response_model=responses.users.Authentication)
def refresh(request: fastapi.Request):
    new_access_token = get_new_access_token(request)
    return {'access_token': new_access_token, "token_type": "Bearer"}