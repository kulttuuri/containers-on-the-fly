from typing import Tuple
import os
import hashlib
import hmac
import random
import string
from database import User, session, UserWhitelist
import helpers.server
import ldap3 as ldap
from settings import settings

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

  Example usage:
    if IsCorrectPassword(hash['salt'], hash['hashedPassword'], 'correct horse battery staple') == True
  """
  return hmac.compare_digest(
    pw_hash,
    hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
  )

def GetLDAPUser(username, password):
  set = settings.login["ldap"]
  useWhitelisting = settings.login["useWhitelist"]
  # Disable certificate checks
  ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
  l = ldap.initialize(set["url"])
  l.set_option(ldap.OPT_NETWORK_TIMEOUT, 6)
  l.set_option(ldap.OPT_TIMEOUT, 6)
  l.set_option(ldap.OPT_REFERRALS, ldap.OPT_OFF)
  print(os.getcwd())
  #l.set_option(ldap.OPT_X_TLS_CACERTFILE, os.getcwd()+"/certificate.pem")

  try:
    l.simple_bind_s(set["usernameFormat"].replace("{username}", username), set["passwordFormat"].replace("{password}", password))
    result = l.search_s(set["ldapDomain"], ldap.SCOPE_SUBTREE, set["searchMethod"].replace("{username}", username), [set["accountField"], set["emailField"]])
    account = result[0][1][set["accountField"]][0].decode("utf-8")
    if account != username:
      print("Wrong username / ldap username association!")
      return False, "Wrong username / ldap username association"
    
    email = result[0][1][set["emailField"]][0].decode("utf-8")
    whitelistEmail = session.query(UserWhitelist).filter( UserWhitelist.email == email ).first()
    if useWhitelisting and whitelistEmail == None:
      return False, "You are not allowed to login (not whitelisted, LDAP)."

    session.commit()
    user = session.query(User).filter( User.email == email ).first()
    # User not found? Create it and return the newly created user
    if user == None:
      print("User created")
      newUser = User(
        email = email
      )
      session.add(newUser)
      session.commit()
      return True, session.query(User).filter( User.email == email ).first()
    # User found? Return it
    else:
      return True, user
  except ldap.INVALID_CREDENTIALS:
    print('Wrong password or username')
    return False, "Wrong username or password."
  except ldap.SERVER_DOWN:
    print("Timeout")
    return False, "Timeout."
  except Exception as e:
    print(e)
    return False, "Unknown error with the LDAP login!"
  return False, "Unknown error."