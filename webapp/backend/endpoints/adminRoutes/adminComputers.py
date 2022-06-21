from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, Response, CheckIp
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.Computer as ComputerFunctionality

router = APIRouter(
    prefix="/api/adminRoutes/adminComputers",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

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
