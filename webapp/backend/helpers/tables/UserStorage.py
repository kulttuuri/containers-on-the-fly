from database import UserStorage, Session, User

# User storage table management functionality
def getUserStorageList(findby):
  '''
Finds user's storage with the given optional filter (email or userId). If no filter is given, returns None.
  Parameters:
    Example usage: Can be used by email or userId
  Returns:
    Found storage.
'''
  with Session() as session:
    found_storages_list = []
    if findby:
      #found_user = session.query(User).filter(User.userId == findby).first()
      found_users = session.query(User).filter(User.userId.like("%"+findby+"%"))
      for found_user in found_users:
        found_storage = session.query(UserStorage).filter(UserStorage.userId == found_user.userId).first()
        found_storages_list.append(found_storage)
      if found_storages_list:
        return found_storages_list
      found_users = session.query(User).filter(User.email.like("%"+findby+"%"))
      for found_user in found_users:
        found_storage = session.query(UserStorage).filter(UserStorage.userId == found_user.userId).first()
        found_storages_list.append(found_storage)
      if found_storages_list:
        return found_storages_list
      return None
    return None
    
""" def getUserStorage(userStorageId):
  if userStorageId:
    found_storage = session.query(UserStorage).filter(UserStorage.userStorageId == userStorageId).first()
    return found_storage
  return None """

def getUserStorages(findby = None):
  '''
  Finds user storage by userId or email. 
    Parameters: can be passed userId or email.
    Returns:
      Parameter is not None: found storage.
      Parameter is None: all storages.
  '''
  with Session() as session:
    all_storages = session.query(UserStorage)
    all_storages_list = []
    
    for storage in all_storages:
      all_storages_list.append(storage)
    if findby is None:
      return all_storages_list
    found_user = session.query(User).filter(User.userId == findby).first()
    if found_user:
      found_storage = session.query(UserStorage).filter(UserStorage.userId == found_user.userId).first()
      return found_storage
    found_user = session.query(User).filter(User.email == findby).first()
    if found_user:
      found_storage = session.query(UserStorage).filter(UserStorage.userId == found_user.userId).first()
      return found_storage
    return None
    
def addUserStorage(userId, maxSpace, maxSpaceFormat):
  '''
  Adds user to the system.
  Parameters:
    email: email
    password: password
  Returns:
    The created user object fetched from database.
  '''
  with Session() as session:
    session.add(
      UserStorage(
        userId = userId,
        maxSpace = maxSpace,
        maxSpaceFormat = maxSpaceFormat
      )
    )
    session.commit()
   
def removeUserStorage(findby):
  '''
  Removes user.
    Parameter:
      Removes by passed parameter as a user (sql.object).
    Returns:
      Nothing.
  '''
  with Session() as session:
    found_storage = getUserStorages(findby)
    if found_storage:
      session.delete(found_storage)
      session.commit()
      return "Success"
    else:
      return

def editUserStorage(findby, new_maxSpace = None, new_maxSpaceFormat = None):
  '''
  Finds storage by userId or email and changes maxSpace and format.
    Optional parameters:
      Example usage: maxSpace - will change space amount, maxSpaceFormat - changes format.
    Returns:
      All found users in a list.
  '''
  with Session() as session:
    if findby is None:
      return None
    
    found_storage = getUserStorages(findby)
    if found_storage is not None:
      if new_maxSpace != None: found_storage.maxSpace = new_maxSpace
      if new_maxSpaceFormat != None: found_storage.maxSpaceFormat = new_maxSpaceFormat
      session.commit()
    else:
      return None