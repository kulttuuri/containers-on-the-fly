from database import User, session
from helpers.server import Response

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
  # TODO: Check user login method, password or AD, also settings.login["allow_password_login"]
  user = session.query(User).filter( User.email == username, User.password == password ).first()
  if user:
    return Response(True, "Login succesfull.", { "loginToken": "gen" })
  else:
    return Response(False, "Email address or password was invalid.", { "loginToken": None })

def check_token(token):
  ''' Checks that the given token is valid and has not expired.

      Parameters:
        token: token
      
      Returns:
        If token was ok, returns also back information about the user.
        Otherwise tells that the user is not currently logged in.
  '''
  return Response(False, "User is not currently logged in.")

def create_password(password):
  ''' For generating encrypted password for a user
      Parameters:
        password: password
  '''
  return password