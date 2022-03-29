from typing import Tuple
import os
import hashlib
import hmac

def IsAdmin(email, token):
  print("WIP: IMPLEMENT ADMIN CHECKING FUNCTIONALITY")
  return False

def IsLoggedIn(email, token):
  print("WIP: IMPLEMENT LOGIN CHECKING FUNCTIONALITY")
  return False

# Taken from here: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/18488878#18488878
def hashPassword(password: str) -> Tuple[bytes, bytes]:
  """
  Hash the provided password with a randomly-generated salt and return the
  salt and hash to store in the database.
  """
  salt = os.urandom(16)
  pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
  return { "salt": salt, "hashedPassword": pw_hash }

# Taken from here: https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python/18488878#18488878
def isCorrectPassword(salt: bytes, pw_hash: bytes, password: str) -> bool:
  """
  Given a previously-stored salt and hash, and a password provided by a user
  trying to log in, check whether the password is correct.
  """
  return hmac.compare_digest(
    pw_hash,
    hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
  )

# Example usage:
#hash = hashPassword('correct horse battery staple')
#assert isCorrectPassword(salt, pw_hash, 'correct horse battery staple')
#assert not isCorrectPassword(salt, pw_hash, 'Tr0ub4dor&3')
#assert not isCorrectPassword(salt, pw_hash, 'rosebud')