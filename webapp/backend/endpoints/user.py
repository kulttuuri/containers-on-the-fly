from fastapi import APIRouter, Depends
from helpers.server import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from endpoints.responses import user

router = APIRouter(
    prefix="/api/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  return user.login(form_data.username, form_data.password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.get("/check_token")
async def checkToken(token: str = Depends(oauth2_scheme)):
  return user.checkToken(token)

@router.post("/create_password")
async def createPassword(password: str):
  return user.createPassword(password)

@router.get("/profile")
async def profile():
  # TODO: Check for auth key from the Authentication header
  return Response(False, "IMPLEMENT")