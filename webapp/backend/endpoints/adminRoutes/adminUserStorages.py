from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, Response, CheckIp
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.UserStorage as UserStorageFunctionality

router = APIRouter(
    prefix="/api/adminRoutes/adminUserStorages",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

#UserStorage API
@router.get("/get_userstorages")
async def getUserStorages(request: Request, findby: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserStorageFunctionality.getUserStorages(findby)

@router.get("/get_userstorage_list")
async def getUserStorageList(request: Request, findby: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserStorageFunctionality.getUserStorageList(findby)

@router.get("/add_userstorage")
async def addUserStorage(request: Request, userId: int, maxSpace: int, maxSpaceFormat: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserStorageFunctionality.addUserStorage(userId, maxSpace, maxSpaceFormat)

@router.get("/remove_userstorage")
async def removeUserStorage(request: Request, findby: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserStorageFunctionality.removeUserStorage(findby)

@router.get("/edit_userstorage")
async def editUserStorage(request: Request, findby: str, new_maxSpace: int = None, new_maxSpaceFormat: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserStorageFunctionality.editUserStorage(findby, new_maxSpace, new_maxSpaceFormat)
