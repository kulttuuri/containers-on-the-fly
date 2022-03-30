from typing import Tuple
import os
import hashlib
import hmac
import random
import string
from database import Role, User, session

def IsAdmin(email):
  user = session.query(User).find( User.email == email )
  isAdmin = False
  for role in user.roles:
    if role.name == "Admin": isAdmin = True
  return isAdmin

# Creates login token of 100 characters (including some special characters)
# and returns it back.
def CreateLoginToken():
  allowedChars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!_-"
  limit = 100
  return ''.join(random.choice(allowedChars) for _ in range(limit))

# Taken from here: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/18488878#18488878
# Example usage:
# hash = HashPassword('correct horse battery staple')
def HashPassword(password: str) -> Tuple[bytes, bytes]:
  """
  Hash the provided password with a randomly-generated salt and return the
  salt and hash to store in the database.
  """
  salt = os.urandom(16)
  pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
  return { "salt": salt, "hashedPassword": pw_hash }

# Taken from here: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/18488878#18488878
# Example usage:
# if IsCorrectPassword(hash['salt'], hash['hashedPassword'], 'correct horse battery staple') == True
def IsCorrectPassword(salt: bytes, pw_hash: bytes, password: str) -> bool:
  """
  Given a previously-stored salt and hash, and a password provided by a user
  trying to log in, check whether the password is correct.
  """
  return hmac.compare_digest(
    pw_hash,
    hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
  )