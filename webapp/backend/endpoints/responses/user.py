from database import User, session
from helpers.server import Response
from settings import settings

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
  if settings.login["allow_password_login"] == False:
    return Response(False, "Password logins are disabled.")
  user = session.query(User).first()
  #user = session.query(User).filter( User.email == username, User.password == password ).first()
  if user:
    return Response(True, "Login succesfull.", { "loginToken": "gen" })
  else:
    return Response(False, "Email address or password was invalid.", { "loginToken": None })

def checkToken(token):
  ''' Checks that the given token is valid and has not expired.

      Parameters:
        token: token
      
      Returns:
        If token was ok, returns also back information about the user.
        Otherwise tells that the user is not currently logged in.
  '''
  return Response(False, "User is not currently logged in.")

def createPassword(password):
  ''' For generating encrypted password for a user
      Parameters:
        password: password
  '''
  return password