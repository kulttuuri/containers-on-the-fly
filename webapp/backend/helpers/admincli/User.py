from helpers.server import *
from settings import settings

def CLIusers():
  breakLoop = False
  while breakLoop == False:
    print(f'\nManaging users {len(CallAdminAPI("get", "adminRoutes/adminUsers/get_users", settings.adminToken))} users in database')
    print("What do you want to do?")
    print("1) List users")
    print("2) Add new user")
    print("3) Remove user")
    print("4) Edit user")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIusersList()
    elif (selection == "2"): CLIAddUser()
    elif (selection == "3"): CLIremoveUser()
    elif (selection == "4"): CLIeditUser()
    elif (selection == "5"): breakLoop = True


def CLIusersList():
  breakLoop = False
  while breakLoop == False:
    print("\nUser Listing")
    print("1) List all users")
    print("2) List users with email containing")
    print("3) Go back")
    selection = input()
    
    if (selection == "1"): CLIPrintAllUsers()
    if (selection == "2"): CLIPrintUsersWithEmail()
    if (selection == "3"): breakLoop = True

def CLIAddUser():
  email = input("To add user enter email: ")
  password = input("Enter password: ")
  duplicate = CallAdminAPI("get", "adminRoutes/adminUsers/get_user", settings.adminToken, params={"findby": email})
  if password == "":
    print("Password cannot be empty!")
  elif duplicate is None:
    CallAdminAPI("get", "adminRoutes/adminUsers/add_user", settings.adminToken, params={"email": email, "password": password})
  else:
    print("User already exists!")
    CallAdminAPI("get", "adminRoutes/adminUsers/add_user", settings.adminToken, params={"email": email, "password": password})

def CLIPrintAllUsers():
  print()
  print("List of all users:")
  users = CallAdminAPI("get", "adminRoutes/adminUsers/get_users", settings.adminToken)
  for user in users:
    print("id:", user["userId"], "- email:", user["email"], "- created at:", user["userCreatedAt"], "- updated at:", user["userUpdatedAt"], "- storage:", len(user["userStorage"]), "- role:", len(user["roles"]), "- reservations:", len(user["reservations"]))

def CLIPrintUsersWithEmail():
  email = input("To find users by email, enter part of the email (to go back enter 3): ")
  found_email_list = CallAdminAPI("get", "adminRoutes/adminUsers/get_users", settings.adminToken, params={"email": email})
  if email == "3":
    return 
  elif found_email_list is None:
    print(f"None of the emails contain '{email}' part.")
    print("Try again.")
    CLIPrintUsersWithEmail()
  else:
    for found_email in found_email_list:
      print("Found users:")
      print("userId:", found_email["userId"], "- email:", found_email["email"], "- created at", found_email["userCreatedAt"], "- updated at:", found_email["userUpdatedAt"], "- storage:", len(found_email["userStorage"]), "- role:", len(found_email["roles"]), "- reservations:", len(found_email["reservations"]))
    
def CLIremoveUser():
  findby = input("Enter userId or email (press Enter to go back): ")
  if findby == "":
    return
  try:
    CallAdminAPI("get", "adminRoutes/adminUserStorages/remove_userstorage", settings.adminToken, params={"findby": findby})
  except:
    worked = CallAdminAPI("get", "adminRoutes/adminUsers/remove_user", settings.adminToken, params={"findby": findby})
    if worked:
      print(f"User {findby} was removed.")
      CLIremoveUser()
  else:
    print("User does not exist!")
    print("Try again.")
    CLIPrintAllUsers()
    CLIremoveUser()

def CLIeditUser():
  print("Do you want change email or password?")
  print("1) Change email")
  print("2) Change password")
  print("3) Go back")
  selection = input()
    
  if (selection == "1"): CLIeditUserEmail()
  if (selection == "2"): CLIeditUserPassword()
  if (selection == "3"): return 
  
def CLIeditUserEmail():
  email = input("Enter email to edit (press Enter go back): ")
  found_email = CallAdminAPI("get", "adminRoutes/adminUsers/get_user", settings.adminToken, params={"findby": email})
  if email == "":
    CLIeditUser()
  elif found_email is None:
    print("Email was not found.")
    print("Try again.")
    CLIeditUserEmail()
  else:
    new_email = input("Enter new email: ")
    CallAdminAPI("get", "adminRoutes/adminUsers/edit_user", settings.adminToken, params={email, {"email": new_email}})
    print("Email was changed.")

def CLIeditUserPassword():
  email = input("Enter email to edit (press Enter to go back): ") 
  found_email = CallAdminAPI("get", "adminRoutes/adminUsers/get_user", settings.adminToken, params={"findby": email})
  if email == "":
    CLIeditUser()
  elif found_email is None:
    print("Email was not found.")
    print("Try again.")
    CLIeditUserPassword()
  else:
    password = input("Enter password: ")
    response = CallAdminAPI("get", "adminRoutes/adminUsers/edit_user", settings.adminToken, params={"email": email, "new_password": password})
    print("Password was changed.")