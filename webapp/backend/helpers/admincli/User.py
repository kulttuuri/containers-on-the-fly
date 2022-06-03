from helpers.tables.User import *
from helpers.tables.Reservation import *

def CLIusers():
  breakLoop = False
  count = CLIcountUsers()
  while breakLoop == False:
    print(f"\nManaging users  ({count} users in database)")
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
  email = input("Enter email: ")
  password = input("Enter password: ")
  if password == "":
    print("Password cannot be empty!")
  else:
    addUser(email, password)

def CLIPrintAllUsers():
  print()
  print("List of all users:")
  users = getUsers()
  for user in users:
    print(user.userId, user.email, user.userCreatedAt, user.userUpdatedAt, len(user.userStorage),len(user.roles), len(user.reservations))

def CLIPrintUsersWithEmail():
  email = input("To find users by email, enter part of the email (to go back enter 3): ")
  found_email_list = getUsers(email)

  if email == "3":
    breakLoop = True
  elif found_email_list is None:
    print(f"None of the emails contain '{email}' part.")
    print("Try again.")
    CLIPrintUsersWithEmail()
  else:
    for found_email in found_email_list:
      print("Found users:", found_email.userId, found_email.email, found_email.userCreatedAt, found_email.userUpdatedAt, len(found_email.userStorage),len(found_email.roles), len(found_email.reservations))
    
def CLIremoveUser():
  userId = input("Enter userId or email (press Enter to go back): ")
  user_found = getUser(userId)

  if userId == "":
    breakLoop = True
  elif user_found is None:
    print("User does not exist!")
    print("Try again or type exit")
    CLIremoveUser()
  else:
    session.delete(user_found)
    session.commit()
    print(f"User {userId} was removed.")

def CLIcountUsers():
  count = 0
  users = getUsers()
  for user in users:
    count+=1
  return count

def CLIeditUser():
  print("Do you want change email or password?")
  print("1) Change email")
  print("2) Change password")
  print("3) Go back")
  selection = input()
    
  if (selection == "1"): CLIeditUserEmail()
  if (selection == "2"): CLIeditUserPassword()
  if (selection == "3"): breakLoop = True
  
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
