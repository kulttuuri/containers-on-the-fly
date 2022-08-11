from database import User, session
from helpers.auth import *

# User table management functionality

def getUsers(email = None):
  '''
Finds users with the given optional filter. If no filter is given, finds all users in the system.
  Parameters:
    Filter: email. Example usage: searches the users by entered part of email.
  Returns:
    All found users in a list.
'''
  all_users_list = [] 
  email_users_list = []
  if email is None:
    all_users = session.query(User).all()
    all_users = castUsersToDict(all_users)
    return all_users
  else:
    email_users = session.query(User).filter(User.email.like("%"+email+"%"))
    for email_user in email_users:
      email_users_list.append(email_user)
    email_users_list = castUsersToDict(email_users_list)
    return email_users_list

def getUser(findby):
  '''
Finds user with the given optional filter (email or userId). If no filter is given, returns None.
  Parameters:
    Example usage: Can be used by email or userId
  Returns:
    Found user.
'''
  if findby:
    found_user = session.query(User).filter(User.email == findby).first()
    if found_user:
      found_user = castUsersToDict([found_user])
      return found_user
    found_user = session.query(User).filter(User.userId == findby).first()
    found_user = castUsersToDict([found_user])
    return found_user
  else:
    return None

def castUsersToDict(user_list):
  all_users = [dict(userId = user.userId, email = user.email, userCreatedAt = user.userCreatedAt, userUpdatedAt = user.userUpdatedAt, roles = user.roles, reservations = user.reservations, userStorage = user.userStorage) for user in user_list]
  return all_users

def addUser(email, password):
  '''
  Adds user to the system.
  Parameters:
    email: email
    password: password
  Returns:
    The created user object fetched from database.
  '''

  hash = HashPassword(password)
  session.add(
    User(
      email = email,
      password = hash["hashedPassword"],
      passwordSalt = hash["salt"]
    )
  )
  session.commit()

def editUser(email, new_email = None, new_password = None):
  '''
Finds user by email and changes email or password.
  Optional parameters:
    Example usage: new_email - will change email, new_password - changes password.
  Returns:
    All found users in a list.
'''
  if email is None:
    return None
  
  user = getUserServerside(email)
  if new_email != None:
    user.email = new_email
  if new_password != None:
    hash = HashPassword(new_password)
    user.password = hash["hashedPassword"]
    user.passwordSalt = hash['salt']
  session.commit()
  return None

def removeUser(findby):
  '''
Removes user.
  Parameter:
    Removes by passed parameter as a user (sql.object).
  Returns:
    Nothing.
'''
  found_user = getUser(findby)
  if found_user:
    session.delete(found_user)
    session.commit()
    return "Success"
  return None

def getUserServerside(search):
  '''
Finds user with given search, only to be used serverside.
  Parameter:
    search = string used to search for user's email.
  Returns:
    Single database object.
'''
  found_user = session.query(User).filter(User.email == search).first()
  return found_user