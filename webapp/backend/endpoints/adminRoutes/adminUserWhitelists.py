from fastapi import APIRouter, Depends, Request
from helpers.server import ForceAuthentication, Response, CheckIp
from helpers.auth import CheckToken
from fastapi.security import OAuth2PasswordBearer
import helpers.tables.UserWhitelist as UserWhitelistFunctionality

router = APIRouter(
    prefix="/api/adminRoutes/adminUserWhitelists",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

#UserWhitelist API
@router.get("/view_all")
async def viewAll(request: Request, opt_filter: str = None, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserWhitelistFunctionality.viewAll(opt_filter)

@router.get("/add_to_whitelist")
async def addToWhitelist(request: Request, emails: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserWhitelistFunctionality.addToWhitelist(emails)

@router.get("/remove_from_whitelist")
async def removeFromWhitelist(request: Request, emails: str, token: str = Depends(oauth2_scheme)):
  ForceAuthentication(token, "admin")
  CheckIp(request.client.host)
  return UserWhitelistFunctionality.removeFromWhitelist(emails)
