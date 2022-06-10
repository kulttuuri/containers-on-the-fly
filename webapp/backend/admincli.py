from helpers.admin import *
from helpers.admincli.Computer import *
from helpers.admincli.Container import *
from helpers.admincli.HardwareSpec import *
from helpers.admincli.Reservation import *
from helpers.admincli.Role import *
from helpers.admincli.User import *
from helpers.admincli.UserStorage import *
from helpers.admincli.UserWhitelist import *
from helpers.server import *
import requests
import json

print("Welcome to AI Reservation Server Admin CLI")

def main():
  breakLoop = False
  token = ""
  while breakLoop == False:
    if token == "":
      print("\nWhat would you like to do?")
      print("1) Login")
      print("2) Exit")
      selection = input()
      if selection == "1":
        print("\nLogin menu:")
        print("What is your username?")
        username = input()
        #username = "aiserveradmin@samk.fi"
        print("What is your password?")
        password = input()
        #password = "test"
      
        # Making a get request
        #Login details: username = aiserveradmin@samk.fi and password = test
        response = requests.post("http://127.0.0.1:8000/api/user/login", data= {"username":username,"password":password})
        if response.ok != False:
          token = json.loads(response.text)["access_token"]
          auth = ForceAuthentication(token, "admin")
          if auth == HTTPException:
            print("Account is not an admin.")
            continue
          else: print("\nLogged in successfully.")
        else:
          print("Login not successful, try again.")
          continue
      elif selection == "2": breakLoop = True
    else:
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
