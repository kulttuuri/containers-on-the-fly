from typing import Union
from fastapi import HTTPException, status
from helpers.auth import IsLoggedIn
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property
from helpers.auth import GetRole
from database import User, session

def Response(status, message, extraData = None):
  response = {
    "status": status,
    "message": message
  }
  if extraData is not None:
    response["data"] = extraData
  return response

def ForceAuthentication(token: str, roleRequired: str = None) -> Union[bool,HTTPException]:
  '''
  Checks if user is logged in by using the token passed.
  Parameters:
    token: Token
    roleRequired: If user is required to be in a specific role, that role should be passed here
  Returns:
    True if is user is logged in, otherwise will raise HTTPException.
  '''
  wrongRole = False
  if (IsLoggedIn(token)):
    if roleRequired is not None:
      user = session.query(User).filter( User.loginToken == token ).first()
      if GetRole(user.email) == roleRequired:
        return True
      else:
        wrongRole = True
    else:
      return True
  
  detailMessage = "Invalid authentication credentials"
  if wrongRole == True:
    detailMessage = detailMessage + " - Wrong role"
  raise HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = detailMessage,
    headers = {"WWW-Authenticate": "Bearer"},
  )

def ORMObjectToDict(self):
    dict_ = {}
    for key in self.__mapper__.c.keys():
        if not key.startswith('_'):
            dict_[key] = getattr(self, key)

    for key, prop in inspect(self.__class__).all_orm_descriptors.items():
        if isinstance(prop, hybrid_property):
            dict_[key] = getattr(self, key)
    return dict_