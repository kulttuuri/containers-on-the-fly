from helpers.admin import *
from helpers.admincli.Computer import *
from helpers.admincli.Container import *
from helpers.admincli.HardwareSpec import *
from helpers.admincli.Reservation import *
from helpers.admincli.Role import *
from helpers.admincli.User import *
from helpers.admincli.UserStorage import *
from helpers.admincli.UserWhitelist import *

print("Welcome to AI Reservation Server Admin CLI")

def main():
  breakLoop = False
  while breakLoop == False:
    print("\nWhat do you want to do?")
    print("You can type these commands to manage the tables:")
    print("users, userstorages, whitelisting, containers, hardwarespecs, reservations, roles, computers")
    print("You can also run: stats, exit")
    selection = input()
    if (selection == "users"): CLIusers()
    if (selection == "userstorages"): CLIuserstorages()
    elif (selection == "whitelisting"): CLIuserwhitelisting()
    elif (selection == "containers"): CLIcontainers()
    elif (selection == "hardwarespecs"): CLIhardwarespecs()
    elif (selection == "reservations"): CLIreservations()
    elif (selection == "roles"): CLIroles()
    elif (selection == "computers"): CLIcomputers()
    elif (selection == "stats"): stats()
    elif (selection == "exit"): breakLoop = True

def stats():
  printStats()

main()
