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

@router.get("/get_all_users")
async def getUsers(request: Request, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserFunctionality.getUsers()

@router.get("/get_user")
async def getUser(request: Request, email: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserFunctionality.getUser(email)

#HardwareSpec API
@router.get("/get_hardwarespecs")
async def getHardwarespecs(request: Request, filter: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return HardwareSpecFunctionality.getHardwarespecs(filter)

@router.get("/add_hardwarespec")
async def addHardwarespec(request: Request, computerId: int, type: str, maxAmount: float, minAmount: float,
                          maxUserAmount: float, defaultUserAmount: float, format: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return HardwareSpecFunctionality.addHardwarespec(computerId, type, maxAmount, minAmount, maxUserAmount, defaultUserAmount, format)

@router.get("/remove_hardwarespec")
async def removeHardwarespec(request: Request, hardwarespec_id: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return HardwareSpecFunctionality.removeHardwarespec(hardwarespec_id)

@router.get("/edit_hardwarespec")
async def editHardwarespec(request: Request, hardwarespec_id: int, new_computer_id: int = None, new_type: str = None, new_max: float = None,
                           new_min: float = None, new_user_max: float = None, new_user_default: float = None, new_format: str = None,
                           token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return HardwareSpecFunctionality.editHardwarespec(hardwarespec_id, new_computer_id, new_type, new_max, new_min, new_user_max, new_user_default, new_format)
