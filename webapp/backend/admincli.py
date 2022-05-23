from helpers.admin import *

print("Welcome to AI Reservation Server Admin CLI")

def main():
  print("What do you want to manage?")
  print("You can manage: users, whitelisting, containers, hardwarespecs, reservations, roles")
  print("Type exit to exit the program")
  selection = input()
  if (selection == "users"): users()

def users():
  print("\nManaging users")
  print("What  do you want to do?")
  print("1) List all users")
    # 1) List all users
    # 2) List users email containing
    # 3) Go back
  print("2) Add new user")
  print("3) Remove user")
  print("4) Edit user")
  print("5) Go back")
  selection = input()

def reservations():
  print("\nManaging reservations")
  print("What  do you want to do?")
  print("1) List all reservations")


main()