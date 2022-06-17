from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, Response, CheckIp
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.User as UserFunctionality
import helpers.tables.Role as RoleFunctionality
import helpers.tables.Computer as ComputerFunctionality
import helpers.tables.Container as ContainerFunctionality
import helpers.tables.HardwareSpec as HardwareSpecFunctionality

router = APIRouter(
    prefix="/api/admin",
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

# Role API
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

# Container API
@router.get("/get_containers")
async def getContainers(request: Request, filter: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ContainerFunctionality.getContainers(filter)

@router.get("/add_container")
async def addContainer(request: Request, name: str, public: bool, description: str, imageName: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ContainerFunctionality.addContainer(name, public, description, imageName)

@router.get("/remove_container")
async def removeContainer(request: Request, container_id: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ContainerFunctionality.removeContainer(container_id)

@router.get("/edit_container")
async def editContainer(request: Request, container_id: int, new_name: str = None, new_public: bool = None, new_description: str = None,
                        new_image_name: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ContainerFunctionality.editContainer(container_id, new_name, new_public, new_description, new_image_name)

# Computer API
@router.get("/get_computers")
async def getComputers(request: Request, filter: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ComputerFunctionality.getComputers(filter)

@router.get("/add_computer")
async def addComputer(request: Request, name: str, public: bool, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ComputerFunctionality.addComputer(name, public)

@router.get("/remove_computer")
async def removeComputer(request: Request, computer_id: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ComputerFunctionality.removeComputer(computer_id)

@router.get("/edit_computer")
async def editComputer(request: Request, computer_id: int, new_name: str = None, new_public: bool = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ComputerFunctionality.editComputer(computer_id, new_name, new_public)

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

# RoleFunctionality ComputerFunctionality ContainerFunctionality HardwareSpecFunctionality