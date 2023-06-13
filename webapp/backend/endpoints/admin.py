from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication
from fastapi.security import OAuth2PasswordBearer
from endpoints.responses import admin as functionality

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/reservations")
async def getReservations(token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  return functionality.getReservations()

@router.get("/users")
async def getUsers(token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  return functionality.getUsers()

@router.get("/hardware")
async def getHardware(token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  return functionality.getHardware()

@router.get("/containers")
async def getContainers(token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  return functionality.getContainers()

@router.post("/edit_reservation")
async def editReservation(reservationId : int, endDate : str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  return functionality.editReservation(reservationId, endDate)

