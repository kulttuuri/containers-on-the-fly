from helpers.tables.User import *

def CLIusers():
  breakLoop = False
  while breakLoop == False:
    print("\nManaging users  (3 users in database)")
    print("What do you want to do?")
    print("1) List users")
    print("2) Add new user")
    print("3) Remove user")
    print("4) Edit user")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIusersList()
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
    if (selection == "1"): CLIPrintUsersWithEmail()
    if (selection == "3"): breakLoop = True

def CLIAddUser():
  print("TODO: Ask user details and call addUser(...) function")
  #addUser()

def CLIPrintAllUsers():
  print("TODO: Print all users here by using the getUsers(...) function")
  users = getUsers()
  for user in users:
    # Print user details here one by one
    print("...")

def CLIPrintUsersWithEmail():
  print("TODO: Ask for email address, try to get users that contain the part of that email. Use getUsers(...) function")