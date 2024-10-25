# Group table management functionality
from database import Group, User, Session

def getGroups(filter = None):
  '''
  Finds groups with the given optional filter. If no filter is given, finds all groups in the system.
    Parameters:
      filter: Additional filters. Example usage: ...
    Returns:
      All found groups in a list.
  '''
  with Session() as session:
    if filter != None:
      groups = session.query(Group).filter(Group.name == filter).first()
      if groups != None: return [groups]
      else:
        try:
          groups = session.query(Group).filter(Group.groupId == int(filter)).first()
          if groups != None: return [groups]
          else: return None
        except:
          return None
    else: groups = session.query(Group).all()
    return groups

def addGroup(name):
  '''
  Adds the given group in the system.
    Parameters:
      name: The name of the group to be added.
    Returns:
      The created group object fetched from database. Or None if provided name already exists.
  '''
  with Session() as session:
    duplicate = session.query(Group).filter(Group.name == name).first()
    if duplicate != None:
      return None
    newGroup = Group(name = name)
    session.add(newGroup)
    session.commit()
    return session.query(Group).filter(Group.name == name).first()

def removeGroup(group_id):
  '''
  Removes the given group in the system.
    Parameters:
      group_id: The id of the group to be removed.
    Returns:
      Nothing
  '''
  with Session() as session:
    group = session.query(Group).filter(Group.groupId == group_id).first()
    session.delete(group)
    session.commit()

def editGroup(group_id, new_name = None):
  '''
  Edits the given group in the system.
    Parameters:
      group_id: The id of the group to be edited.
      new_name: The new name for the given group.
    Returns:
      The edited group object fetched from database. Or None if name isn't provided.
  '''
  with Session() as session:
    group = session.query(Group).filter(Group.groupId == group_id).first()
    if new_name != None: group.name = new_name
    session.commit()
    return group

def addUserToGroup(group_id, user_id):
  '''
  Adds a user to the given group in the system.
    Parameters:
      group_id: The id of the group.
      user_id: The id of the user to be added to the group.
    Returns:
      The updated group object fetched from database.
  '''
  with Session() as session:
    group = session.query(Group).filter(Group.groupId == group_id).first()
    user = session.query(User).filter(User.userId == user_id).first()
    group.users.append(user)
    session.commit()
    return group

def removeUserFromGroup(group_id, user_id):
  '''
  Removes a user from the given group in the system.
    Parameters:
      group_id: The id of the group.
      user_id: The id of the user to be removed from the group.
    Returns:
      The updated group object fetched from database.
  '''
  with Session() as session:
    group = session.query(Group).filter(Group.groupId == group_id).first()
    user = session.query(User).filter(User.userId == user_id).first()
    group.users.remove(user)
    session.commit()
    return group
