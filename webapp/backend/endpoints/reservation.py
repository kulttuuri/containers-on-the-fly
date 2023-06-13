from fastapi import APIRouter, Depends
from helpers.server import Response, ForceAuthentication
from helpers.auth import CheckToken, IsAdmin
from fastapi.security import OAuth2PasswordBearer
from endpoints.responses import reservation as functionality
import json

router = APIRouter(
    prefix="/api/reservation",
    tags=["Reservation"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/get_available_hardware")
async def getAvailableHardware(date : str, duration: int, token: str = Depends(oauth2_scheme)):
  userId = CheckToken(token)["data"]["userId"]
  return functionality.getAvailableHardware(date, duration, None, IsAdmin(userId))

@router.get("/get_own_reservations")
async def getOwnReservations(token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  userId = CheckToken(token)["data"]["userId"]
  return functionality.getOwnReservations(userId)

@router.get("/get_own_reservation_details")
async def getOwnReservations(reservationId: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  userId = CheckToken(token)["data"]["userId"]
  return functionality.getOwnReservationDetails(reservationId, userId)

@router.post("/create_reservation")
async def CreateReservation(date: str, duration: int, computerId: int, containerId: int, hardwareSpecs, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  try:
    hardwareSpecs = json.loads(hardwareSpecs)
  except:
    return Response(False, "Error.")
  
  userId = CheckToken(token)["data"]["userId"]
  return functionality.createReservation(userId, date, duration, computerId, containerId, hardwareSpecs)

@router.get("/get_current_reservations")
async def getCurrentReservations(token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  return functionality.getCurrentReservations()

@router.post("/cancel_reservation")
async def cancelReservation(reservationId: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  userId = CheckToken(token)["data"]["userId"]
  return functionality.cancelReservation(userId, reservationId)

@router.post("/restart_container")
async def RestartContainer(reservationId: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  userId = CheckToken(token)["data"]["userId"]
  return functionality.restartContainer(userId, reservationId)