# Role table management functionality
from database import Role, session

def getRoles(filter = None):
  '''
  Finds roles with the given optional filter. If no filter is given, finds all roles in the system.
    Parameters:
      filter: Additional filters. Example usage: ...
    Returns:
      All found roles in a list.
  '''
  if filter != None:
    roles = session.query(Role).filter(Role.name == filter).first()
    if roles != None: return [roles]
    else:
      try:
        roles = session.query(Role).filter(Role.roleId == int(filter)).first()
        if roles != None: return [roles]
        else: return None
      except:
        return None
  else: roles = session.query(Role).all()
  return roles

def addRole(name):
  '''
  Adds the given role in the system.
    Parameters:
      name: The name of the role to be added.
    Returns:
      The created role object fetched from database. Or None if provided name already exists.
  '''
  duplicate = session.query(Role).filter(Role.name == name).first()
  if duplicate != None:
      return None
  newRole = Role(name = name)
  session.add(newRole)
  session.commit()
  return session.query(Role).filter(Role.name == name).first()

def removeRole(role):
  '''
  Removes the given role in the system.
    Parameters:
      role: The role object of the role to be removed.
    Returns:
      Nothing
  '''
  session.delete(role)
  session.commit()

def editRole(role, new_name):
  '''
  Edits the given role in the system.
    Parameters:
      role: The role object of the role to be edited.
      new_name: The new name for the given role. #is this too hardcoded..?
    Returns:
      The edited role object fetched from database.
  '''
  role.name = new_name
  session.commit()
  return role