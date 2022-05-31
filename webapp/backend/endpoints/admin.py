from fastapi import APIRouter, Depends
from helpers.server import Response, ForceAuthentication
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.User as UserFunctionality

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/get_all_users")
async def getUsers(token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  return UserFunctionality.getUsers()

@router.get("/get_user")
async def getUser(email: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  return UserFunctionality.getUser(email)