from inspect import Traceback
from helpers.tables.UserStorage import *
from helpers.tables.User import *
from helpers.admincli.User import *
from helpers.server import *
from settings import settings

def CLIuserstorages():
  breakLoop = False
  while breakLoop == False:
    storages = CallAdminAPI("get", "adminRoutes/adminUserStorages/get_userstorages", settings.adminToken)
    print(f"\nManaging user storages ({len(storages)} storages in database)")
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
  storages = CallAdminAPI("get", "adminRoutes/adminUserStorages/get_userstorages", settings.adminToken)
  for storage in storages:
    print("user storage id:", storage["userStorageId"], "- userId:", storage["userId"], "- maxSpace:", storage["maxSpace"], "- maxSpaceFormat:", storage["maxSpaceFormat"], "- created at:", storage["createdAt"], "- updated at:", storage["updatedAt"])
  print()
  print("List of emails and userId's and storage ID's:")
  users = CallAdminAPI("get", "adminRoutes/adminUsers/get_users", settings.adminToken)
  for user in users:
    found_storage = CallAdminAPI("get", "adminRoutes/adminUserStorages/get_userstorages", settings.adminToken, params={"findby": user["userId"]})
    try:
      print("email:", user["email"], "UserId:", user["userId"], "ID:", found_storage["userStorageId"])
    except:
      print("email:", user["email"], "UserId:", user["userId"], "ID:", None)
      
def CLIPrintUserStoragesBy():
  findby = input("To find storage enter userId or email (press Enter to go back): ")
  found_storages = CallAdminAPI("get", "adminRoutes/adminUserStorages/get_userstorage_list", settings.adminToken, params={"findby": findby})
  if findby == "":
    CLIuserstorages()
  elif found_storages is None or found_storages == [None]:
    print(f"None of the storages with {findby} was found.")
    print("Try again.")
    CLIPrintUserStoragesBy()
  else:
    for found_storage in found_storages:
      print("Found storage:")
      print("user storage id:", found_storage["userStorageId"], "- userId:", found_storage["userId"], "- maxSpace:", found_storage["maxSpace"], "- maxSpaceFormat:", found_storage["maxSpaceFormat"], "- created at:", found_storage["createdAt"], "- updated at:", found_storage["updatedAt"])
    return findby

def CLIAddUserStorage():
  userId = input("To add storage enter userId ((press Enter to go back): ")
  storage_found = CallAdminAPI("get", "adminRoutes/adminUserStorages/get_userstorages", settings.adminToken, params={"findby": userId})
  if userId == "":
    return
  elif storage_found:
    print(f"UserStorage with id = {userId} already exists!")
    CLIAddUserStorage()
  else:
    try:
      userId = int(userId)
    except ValueError:
      print("Invalid userId. Should be an integer!")
      CLIAddUserStorage()
    user_found = CallAdminAPI("get", "adminRoutes/adminUsers/get_user", settings.adminToken, params={"findby": userId})
    if user_found is not None:
      while True:
        try:
          maxSpace = int(input("maxSpace: "))
        except ValueError:
          print("Invalid input! Enter integers.")
          continue
        while True:
          maxSpaceFormat = input("maxSpaceFormat (mb/gb): ")
          if maxSpaceFormat == "mb" or maxSpaceFormat == "gb":
            CallAdminAPI("get", "adminRoutes/adminUserStorages/add_userstorage", settings.adminToken, params={"userId": userId, "maxSpace": maxSpace, "maxSpaceFormat": maxSpaceFormat})
            print("UserStorage was created.")
            CLIAddUserStorage()
            break
          else:
            continue
        break
    else:
      print(f"User {userId} does not exist!")
      print("You can check all the users here:")
      CLIPrintAllUsers()
      CLIAddUserStorage()
  

def CLIremoveUserStorage():
  findby = input("Enter userId or email (press Enter to go back): ")
  if findby == "":
    return
  worked = CallAdminAPI("get", "adminRoutes/adminUserStorages/remove_userstorage", settings.adminToken, params={"findby": findby})
  if worked:
    print(f"Storage with id = {findby} was removed.")
    CLIremoveUserStorage()
  else:
    print("Storage does not exist!")
    print("Try again.")
    CLIPrintAllUserStorages()
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
      CallAdminAPI("get", "adminRoutes/adminUserStorages/edit_userstorage", settings.adminToken, params={findby, {"maxSpace": maxSpace}})
      if maxSpaceFormat == "gb" or maxSpaceFormat == "mb":
        editUserStorage(findby, {"maxSpaceFormat": maxSpaceFormat})
        CallAdminAPI("get", "adminRoutes/adminUserStorages/edit_userstorage", settings.adminToken, params={findby, {"maxSpaceFormat": maxSpaceFormat}})
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
  