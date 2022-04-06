from fastapi import APIRouter, Depends
from helpers.server import Response, ForceAuthentication
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
from endpoints.responses import reservation as functionality
from pydantic import BaseModel
from typing import List
import json

router = APIRouter(
    prefix="/api/reservation",
    tags=["Reservation"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

@router.get("/get_available_hardware")
async def getAvailableHardware(date : str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token)
  return functionality.getAvailableHardware(date)

@router.post("/create_reservation")
async def getAvailableHardware(date: str, duration: int, computerId: int, hardwareSpecs, token: str = Depends(oauth2_scheme)):
  try:
    ForceAuthentication(token)
    hardwareSpecs = json.loads(hardwareSpecs)
    userId = CheckToken(token)["data"]["userId"]
    return functionality.createReservation(userId, date, duration, computerId, hardwareSpecs)
  except:
    return Response(False, "Error.")