from typing import Union
from fastapi import HTTPException, status
from helpers.auth import IsLoggedIn
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property

def Response(status, message, extraData = None):
  response = {
    "status": status,
    "message": message
  }
  if extraData is not None:
    response["data"] = extraData
  return response

def ForceAuthentication(token: str) -> Union[bool,HTTPException]:
  '''
  Checks if user is logged in by using the token passed.
  Returns:
    True if is user is logged in, otherwise will raise HTTPException.
  '''
  if (IsLoggedIn(token)): return True
  else:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid authentication credentials",
      headers={"WWW-Authenticate": "Bearer"},
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