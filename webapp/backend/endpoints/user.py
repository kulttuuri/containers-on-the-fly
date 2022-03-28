from fastapi import APIRouter
from database import User, session
from helpers.server import Response
from settings import settings

router = APIRouter(
    prefix="/api/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get("/login")
async def login(email: str, password: str):
  # TODO: Check user login method, password or AD, also settings.login["allow_password_login"]
  user = session.query(User).filter( User.email == email, User.password == password ).first()
  if user:
    return Response(True, "Login succesfull.", { "token": "gen" })
  else:
    return Response(False, "Failed to login.", { "token": "none" })

@router.get("/profile")
async def profile():
  # TODO: Check for auth key from the Authentication header
  return Response(False, "IMPLEMENT")