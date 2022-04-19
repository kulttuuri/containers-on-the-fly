from database import User, session, UserWhitelist
from helpers.server import Response
from settings import settings
from helpers.auth import CreateLoginToken, HashPassword, IsCorrectPassword, CheckToken, GetLDAPUser
from fastapi import HTTPException, status
from datetime import datetime

def login(username, password):
  '''
    Logins the user with the given username and password, if password logins are enabled.
      Parameters:
        username: Email address
        password: Password
      
      Returns:
        If login was succesfull, will return back the generated token that user can use further on.
        Otherwise tells that the username or password was invalid.
  '''
  if username == "" or username is None: raise HTTPException(status_code=400, detail="username cannot be empty.")
  if password == "" or password is None: raise HTTPException(status_code=400, detail="password cannot be empty.")

  user = None
  loginType = settings.login["loginType"]
  useWhitelisting = settings.login["useWhitelist"]

  if loginType == "password":
    user = session.query(User).filter( User.email == username).first()
  elif loginType == "LDAP":
    ldapSuccess, response = GetLDAPUser(username, password)
    if ldapSuccess == False:
      return Response(False, response)
    user = response

  whitelistEmail = session.query(UserWhitelist).filter( UserWhitelist.email == username ).first()
  if loginType == "password" and useWhitelisting and whitelistEmail == None:
    return Response(False, "You are not allowed to login (not whitelisted).")

  # User found
  if user:
    # Check that the password is correct (only for password logins)
    if loginType == "password" and IsCorrectPassword(user.passwordSalt, user.password, password) == False:
      raise HTTPException(status_code=400, detail="Incorrect password.")

    # Create login token and return it
    user.loginToken = CreateLoginToken()
    user.loginTokenCreatedAt = datetime.utcnow()
    session.commit()
    return {
      "access_token": user.loginToken,
      "token_type": "bearer"
    }
  # User not found, invalid login credentials
  else:
    raise HTTPException(status_code=400, detail="User not found.")

def checkToken(token):
  ''' Checks that the given token is valid and has not expired.

      Parameters:
        token: token
      
      Returns:
        If token was ok, returns also back information about the user.
        Otherwise tells that the user is not currently logged in.
  '''
  tokenCheck = CheckToken(token)

  if (tokenCheck["status"] == True): return tokenCheck
  else:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid authentication credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )

def createPassword(password):
  ''' For generating encrypted password for a user
      Parameters:
        password: password
  '''
  if password == "" or password is None:
    return Response(False, "Password cannot be empty.")
  hash = HashPassword(password)
  return Response(True, "Password created", {
    "password": str(hash["hashedPassword"]),
    "salt": str(hash['salt'])
  })