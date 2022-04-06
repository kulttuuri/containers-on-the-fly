from fastapi import APIRouter, Depends
from helpers.server import Response, ForceAuthentication
from fastapi.security import OAuth2PasswordBearer
from endpoints.responses import reservation as functionality

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