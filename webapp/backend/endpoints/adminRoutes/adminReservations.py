from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, Response, CheckIp
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.Reservation as ReservationFunctionality
from datetime import datetime

router = APIRouter(
    prefix="/api/adminRoutes/adminReservations",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.get("/get_reservations")
async def getReservations(request: Request, filter: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ReservationFunctionality.getReservations(filter)

@router.get("/get_reservation")
async def getReservation(request: Request, filter: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ReservationFunctionality.getReservation(filter)

@router.get("/add_reservation")
async def addReservation(request: Request, startDate: datetime, endDate: datetime, userId: int, computerId: int,
                         containerId: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ReservationFunctionality.addReservation(startDate, endDate, userId, computerId, containerId)

@router.get("/remove_reservation")
async def removeReservation(request: Request, reservation_id: int, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ReservationFunctionality.removeReservation(reservation_id)

@router.get("/edit_reservation")
async def editReservation(request: Request, reservation_id: int, new_startDate: datetime = None, new_endDate: datetime = None,
                          new_status: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return ReservationFunctionality.editReservation(reservation_id, new_startDate, new_endDate, new_status)
