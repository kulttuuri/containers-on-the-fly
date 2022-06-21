from helpers.tables.UserStorage import *
from helpers.tables.User import *
from helpers.admincli.User import *

def CLIuserStorages():
  breakLoop = False
  while breakLoop == False:
    print(f"\nManaging user storages ({len(getUserStorages())} storages in database)")
    print("1) List storages")
    print("2) Add new storage")
    print("3) Remove storage")
    print("4) Edit storage")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIuserStorageList()
    elif (selection == "2"): CLIAddUserStorage()
    elif (selection == "3"): CLIremoveUserStorage()
    elif (selection == "4"): CLIeditUserStorage()
    elif (selection == "5"): breakLoop = True

def CLIuserStorageList():
  breakLoop = False
  while breakLoop == False:
    print("\nStorage Listing")
    print("1) List all storages")
    print("2) List storages by userId or email")
    print("3) Go back")
    selection = input()
    
    if (selection == "1"): CLIPrintAllUserStorages()
    if (selection == "2"): CLIPrintUserStoragesBy()
    if (selection == "3"): breakLoop = True

def CLIPrintAllUserStorages():
  print()
  print("List of all storages:")
  storages = getUserStorages()
  for storage in storages:
    print("user storage id:", storage.userStorageId, "- userId:", storage.userId, "- maxSpace:", storage.maxSpace, "- maxSpaceFormat:", storage.maxSpaceFormat, "- created at:", storage.createdAt, "- updated at:", storage.updatedAt)
  print()
  print("List of user emails and storage ID's:")
  users = getUsers()
  for user in users:
    found_storage = session.query(UserStorage).filter(UserStorage.userId == user.userId).first()
    try:
      print("email:", user.email, "ID:", found_storage.userStorageId)
    except AttributeError:
      print("email:", user.email, "ID:", None)
      
def CLIPrintUserStoragesBy():
  findby = input("To find storage enter userId or email (press Enter to go back): ")
  found_storages = getUserStorageList(findby)
  if findby == "":
    CLIuserStorages()
  elif found_storages is None or found_storages == [None]:
    print(f"None of the storages with {findby} was found.")
    print("Try again.")
    CLIPrintUserStoragesBy()
  else:
    for found_storage in found_storages:
      print("Found storage:")
      print("user storage id:", found_storage.userStorageId, "- userId:", found_storage.userId, "- maxSpace:", found_storage.maxSpace, "- maxSpaceFormat:", found_storage.maxSpaceFormat, "- created at:", found_storage.createdAt, "- updated at:", found_storage.updatedAt)
    return findby

def CLIAddUserStorage():
  userId = input("To add storage enter userId ((press Enter to go back): ")
  if userId == "":
    return
  try:
    userId = int(userId)
  except ValueError:
    print("Invalid userId. Should be an integer!")
    CLIAddUserStorage()
  if getUser(userId) is not None:
    while True:
      try:
        maxSpace = int(input("maxSpace: "))
      except ValueError:
        print("Invalid input! Enter integers.")
        continue
      while True:
        maxSpaceFormat = input("maxSpaceFormat (mb/gb): ")
        if maxSpaceFormat == "mb" or maxSpaceFormat == "gb":
          print("UserStorage was created.")
          addUserStorage(userId, maxSpace, maxSpaceFormat)
          break
        else:
          print("continue from fromat:")
          continue
      break
  else:
    print(f"User {userId} does not exist!")
    print("You can check all the users here:")
    CLIPrintAllUsers()
  CLIAddUserStorage()

def CLIremoveUserStorage():
  findby = input("Enter userId or email (press Enter to go back): ")
  storage_found = getUserStorages(findby)

  if findby == "":
    return
  elif storage_found is None:
    print("Storage does not exist!")
    print("Try again.")
    CLIPrintAllUserStorages()
    CLIremoveUserStorage()
  else:
    removeUserStorage(storage_found)
    print(f"Storage with id = {findby} was removed.")
    CLIremoveUserStorage()

def CLIeditUserStorage():
  CLIPrintAllUserStorages()
  print()
  #findby = input("Enter userId or email to edit (press Enter to go back): ") 
  #found_storage = getUserStorages(findby)
  print()
  findby = CLIPrintUserStoragesBy()
  print()
  #if findby == "":
    #CLIuserStorages()
  #elif found_storage is None:
    #print("Storage was not found.")
    #print("Try again.")
    #CLIeditUserStorage()
  if findby:
    maxSpace = input("Enter maxSpace integer: ")
    maxSpaceFormat = input("Enter maxSpaceFormat gb or mb: ")
    try: 
      maxSpace = int(maxSpace)
      editUserStorage(findby, {"maxSpace": maxSpace})
      if maxSpaceFormat == "gb" or maxSpaceFormat == "mb":
        editUserStorage(findby, {"maxSpaceFormat": maxSpaceFormat})
        print("UserStorage was changed.")
        CLIeditUserStorage()
      else:
        print("maxSpaceFormat should be mb or gb.")
        print("Try again.")
        CLIeditUserStorage()
    except ValueError:
      print("maxSpace should be integer.")
      print("Try again.")
      CLIeditUserStorage()
  return None
  