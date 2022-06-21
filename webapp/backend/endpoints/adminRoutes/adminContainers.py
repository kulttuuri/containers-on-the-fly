from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, Response, CheckIp
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.Container as ContainerFunctionality

router = APIRouter(
    prefix="/api/adminRoutes/adminContainers",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

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
  