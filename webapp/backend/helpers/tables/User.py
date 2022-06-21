#from helpers.auth import *
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
    all_users = session.query(User)
    for user in all_users:
    #print(user.email)
      all_users_list.append(user)
    #session.commit()
    return all_users_list
  else:
    email_users = session.query(User).filter(User.email.like("%"+email+"%"))
    for email_user in email_users:
      email_users_list.append(email_user)
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
      return found_user
    found_user = session.query(User).filter(User.userId == findby).first()
    return found_user
  else:
    return None

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


def editUser(email, fields):
  '''
Finds user by email and changes email or password.
  Optional parameters:
    Example usage: new_email - will change email, password - changes password.
  Returns:
    All found users in a list.
'''
  if email is None:
    return None
  
  found_user = getUser(email)
  if found_user is not None:
    try:
      #fields["email"]
      # TODO: Check that no other user has this email set
      found_user_new = session.query(User).filter(User.email == fields["email"]).first()
      if found_user_new is None:
        found_user.email = fields["email"]
    except KeyError: 
      #fields["password"]
      #TODO: set user password
      found_user.password = fields["password"]
    session.commit()
  else:
    return None

def removeUser(found_user):
  '''
Removes user.
  Parameter:
    Removes by passed parameter as a user (sql.object).
  Returns:
    Nothing.
'''
  session.delete(found_user)
  session.commit()