from typing import Tuple
import os
import hashlib
import hmac
import random
import string
from database import User, session
import helpers.server

def IsAdmin(email : str) -> bool:
  '''
  Checks that the user with the given email address is in admin role.
  Returns:
    true if is admin, false otherwise.
  '''
  user = session.query(User).find( User.email == email )
  isAdmin = False
  for role in user.roles:
    if role.name == "Admin": isAdmin = True
  return isAdmin

def IsLoggedIn(token : str):
  '''
  Checks if the passed token can be found from the database and has not expired.
  Parameters:
    token: token
  Returns:
    True if user is logged in, false otherwise.
  '''
  tokenResponse = CheckToken(token)
  if (tokenResponse["status"] == True): return True
  else: return False

def CheckToken(token : str) -> object:
  '''
  Checks that the given token is valid and has not expired.
  Parameters:
    token: token
  Returns:
    Returns back a Response.
  Example return:
    { success: True, message: "Token OK.", data: { email: "test", "studentId": "test" } }
  '''
  if token == "" or token is None: return helpers.server.Response(False, "Token cannot be empty.")
  user = session.query(User).filter( User.loginToken == token ).first()

  # TODO: Add also timeouts for tokens, like 24 hours... Configurable through settings.json

  if user is not None:
    return helpers.server.Response(True, "Token OK.", { "userId": user.userId, "email": user.email, "studentId": user.studentId })
  else:
    return helpers.server.Response(False, "Invalid token.")

def CreateLoginToken() -> str:
  '''
  Creates login token of 100 characters (including some special characters)
  and returns it back.
    Returns:
      the generated loginToken
  '''
  allowedChars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!_-"
  limit = 100
  return ''.join(random.choice(allowedChars) for _ in range(limit))

def HashPassword(password: str) -> Tuple[bytes, bytes]:
  """
  Hash the provided password with a randomly-generated salt and return the
  salt and hash to store in the database.
  
  Taken from here: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/18488878#18488878
  
  Example usage:
    hash = HashPassword('correct horse battery staple')
  """
  salt = os.urandom(16)
  pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
  return { "salt": salt, "hashedPassword": pw_hash }

def IsCorrectPassword(salt: bytes, pw_hash: bytes, password: str) -> bool:
  """
  Given a previously-stored salt and hash, and a password provided by a user
  trying to log in, check whether the password is correct.

  Taken from here: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/18488878#18488878

  Example usage:
    if IsCorrectPassword(hash['salt'], hash['hashedPassword'], 'correct horse battery staple') == True
  """
  return hmac.compare_digest(
    pw_hash,
    hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
  )