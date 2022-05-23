from helpers.admin import *
from helpers.tables.User import *

print("Welcome to AI Reservation Server Admin CLI")

def main():
  breakLoop = False
  while breakLoop == False:
    print("\nWhat do you want to do?")
    print("You can type these commands to manage the tables:")
    print("users, userstorages, whitelisting, containers, hardwarespecs, reservations, roles, computers")
    print("You can also run: stats, exit")
    selection = input()
    if (selection == "users"): users()
    elif (selection == "reservations"): reservations()
    elif (selection == "whitelisting"): whitelisting()
    elif (selection == "stats"): stats()
    elif (selection == "exit"): breakLoop = True

def users():
  breakLoop = False
  while breakLoop == False:
    print("\nManaging users")
    print("What do you want to do?")
    print("1) List users")
    print("2) Add new user")
    print("3) Remove user")
    print("4) Edit user")
    print("5) Go back")
    selection = input()

    if (selection == "1"): usersList()
    elif (selection == "5"): breakLoop = True

def usersList():
  breakLoop = False
  while breakLoop == False:
    print("\nUser Listing")
    print("1) List all users")
    print("2) List users with email containing")
    print("3) Go back")
    selection = input()
    
    if (selection == "3"): breakLoop = True

def whitelisting():
  breakLoop = False
  while breakLoop == False:
    print("\nWhitelisting")
    print("1) View all users in the whitelist")
    print("2) Add user to whitelist")
    print("3) Remove user from whitelist")
    print("4) Go back")
    selection = input()

    if (selection == "4"): breakLoop = True

def stats():
  printStats()

def reservations():
  breakLoop = False
  while breakLoop == False:
    print("\nManaging reservations")
    print("What do you want to do?")
    print("1) List all reservations")
    print("2) List all reservations")
    selection = input()
    
    if (selection == "3"): breakLoop = True

main()