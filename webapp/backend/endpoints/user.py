from fastapi import APIRouter, Depends
from helpers.server import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from endpoints.responses import user

router = APIRouter(
    prefix="/api/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

security = HTTPBasic()
@router.get("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
  return user.login(credentials.username, credentials.password)

@router.get("/check_token")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
  return user.checkToken(credentials.password)

@router.get("/create_password")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
  return user.createPassword(credentials.password)



@router.get("/profile")
async def profile():
  # TODO: Check for auth key from the Authentication header
  return Response(False, "IMPLEMENT")