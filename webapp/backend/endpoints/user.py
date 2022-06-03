from fastapi import APIRouter, Depends
from helpers.server import Response, ForceAuthentication
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from endpoints.responses import user as functionality

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

router = APIRouter(
    prefix="/api/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  return functionality.login(form_data.username, form_data.password)

@router.get("/check_token")
async def checkToken(token: str = Depends(oauth2_scheme)):
  return functionality.checkToken(token)

@router.post("/create_password")
async def createPassword(password: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  return functionality.createPassword(password)

@router.get("/profile")
async def profile(token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  return functionality.profile(token)