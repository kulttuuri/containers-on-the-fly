from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, Response, CheckIp
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.Role as RoleFunctionality

router = APIRouter(
    prefix="/api/adminRoutes/adminRoles",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/get_roles")
async def getRoles(request: Request, filter: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return RoleFunctionality.getRoles(filter)

@router.get("/add_role")
async def addRole(request: Request, name: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return RoleFunctionality.addRole(name)

@router.get("/remove_role")
async def removeRole(request: Request, role_id: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return RoleFunctionality.removeRole(role_id)

@router.get("/edit_role")
async def editRole(request: Request, role_id: int, new_name: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return RoleFunctionality.editRole(role_id, new_name)
