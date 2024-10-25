from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, CheckIp
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.Group as GroupFunctionality

router = APIRouter(
    prefix="/api/adminRoutes/adminGroups",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/get_groups")
async def getGroups(request: Request, filter: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return GroupFunctionality.getGroups(filter)

@router.get("/add_group")
async def addGroup(request: Request, name: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return GroupFunctionality.addGroup(name)

@router.get("/remove_group")
async def removeGroup(request: Request, group_id: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return GroupFunctionality.removeGroup(group_id)

@router.get("/edit_group")
async def editGroup(request: Request, group_id: int, new_name: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return GroupFunctionality.editGroup(group_id, new_name)

@router.get("/add_user_to_group")
async def addUserToGroup(request: Request, group_id: int, user_id: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return GroupFunctionality.addUserToGroup(group_id, user_id)

@router.get("/remove_user_from_group")
async def removeUserFromGroup(request: Request, group_id: int, user_id: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return GroupFunctionality.removeUserFromGroup(group_id, user_id)
