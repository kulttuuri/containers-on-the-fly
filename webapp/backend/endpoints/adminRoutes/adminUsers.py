from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, Response, CheckIp
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.User as UserFunctionality

router = APIRouter(
    prefix="/api/adminRoutes/adminUsers",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/get_users")
async def getUsers(request: Request, email: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserFunctionality.getUsers(email)

@router.get("/get_user")
async def getUser(request: Request, findby: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserFunctionality.getUser(findby)

@router.get("/add_user")
async def addUser(request: Request, email: str, password: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserFunctionality.addUser(email, password)

@router.get("/remove_user")
async def removeUser(request: Request, findby: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserFunctionality.removeUser(findby)

@router.get("/edit_user")
async def editUser(request: Request, email: str, new_email: str = None, new_password: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserFunctionality.editUser(email, new_email, new_password)
