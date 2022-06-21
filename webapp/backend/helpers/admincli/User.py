from helpers.tables.User import *
from helpers.tables.Reservation import * 
from helpers.tables.UserStorage import *

def CLIusers():
  breakLoop = False
  count = CLIcountUsers()
  while breakLoop == False:
    print(f"\nManaging users  {len(getUsers())} users in database")
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
  duplicate = getUser(email)
  if password == "":
    print("Password cannot be empty!")
  elif duplicate is None:
    addUser(email, password)
  else:
    print("User already exists!")
    CLIAddUser()

def CLIPrintAllUsers():
  print()
  print("List of all users:")
  users = getUsers()
  for user in users:
    print("id:", user.userId, "- email:", user.email, "- created at:", user.userCreatedAt, "- updated at:", user.userUpdatedAt, "- storage:", len(user.userStorage), "- role:", len(user.roles), "- reservations:", len(user.reservations))

def CLIPrintUsersWithEmail():
  email = input("To find users by email, enter part of the email (to go back enter 3): ")
  found_email_list = getUsers(email)

  if email == "3":
    return 
  elif found_email_list is None:
    print(f"None of the emails contain '{email}' part.")
    print("Try again.")
    CLIPrintUsersWithEmail()
  else:
    for found_email in found_email_list:
      print("Found users:")
      print("userId:", found_email.userId, "- email:", found_email.email, "- created at", found_email.userCreatedAt, "- updated at:", found_email.userUpdatedAt, "- storage:", len(found_email.userStorage), "- role:", len(found_email.roles), "- reservations:", len(found_email.reservations))
    
def CLIremoveUser():
  findby = input("Enter userId or email (press Enter to go back): ")
  user_found = getUser(findby)

  if findby == "":
    return 
  elif user_found is None:
    print("User does not exist!")
    print("Try again.")
    CLIremoveUser()
  else:
    removeUser(user_found)
    print(f"User {findby} was removed.")

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
  found_email = getUser(email)
  if email == "":
    CLIeditUser()
  elif found_email is None:
    print("Email was not found.")
    print("Try again.")
    CLIeditUserEmail()
  else:
    new_email = input("Enter new email: ")
    editUser(email, {"email": new_email})
    print("Email was changed.")

def CLIeditUserPassword():
  email = input("Enter email to edit (press Enter to go back): ") 
  found_email = getUser(email)
  if email == "":
    CLIeditUser()
  elif found_email is None:
    print("Email was not found.")
    print("Try again.")
    CLIeditUserPassword()
  else:
    password = input("Enter password: ")
    editUser(email, {"password": password})
    print("Password was changed.")