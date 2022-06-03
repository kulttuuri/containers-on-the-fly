from helpers.server import Response
# User table management functionality

def getUsers(filter = None):
  '''
  Finds users with the given optional filter. If no filter is given, finds all users in the system.
    Parameters:
      filter: Additional filters. Example usage: ...
    Returns:
      All found users in a list.
  '''
  return Response(True, "Got users", { "users": [], "userCount": 3 })

def addUser():
  '''
  Adds the given user in the system.
    Parameters:
      ...: ...
    Returns:
      The created user object fetched from database.
  '''
  print("TODO: Add user here. Need to pass all required details as function parameters.")
  print("Optional details can be set to default value None or ''")