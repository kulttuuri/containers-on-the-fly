from helpers.tables.Computer import *
from helpers.server import *
from settings import settings

def CLIcomputers():
  breakLoop = False
  while breakLoop == False:
    print(f'\nManaging computers  ({len(CallAdminAPI("get", "adminRoutes/adminComputers/get_computers", settings.adminToken)) } computers in database)')
    print("What do you want to do?")
    print("1) List computers")
    print("2) Add new computer")
    print("3) Remove computer")
    print("4) Edit computer")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIcomputersList()
    elif (selection == "2"): CLIaddComputer()
    elif (selection == "3"): CLIremoveComputer()
    elif (selection == "4"): CLIeditComputer()
    elif (selection == "5"): breakLoop = True

def CLIcomputersList():
  breakLoop = False
  while breakLoop == False:
    print("\nComputer Listing")
    print("1) List all computers")
    print("2) List computer by search")
    print("3) Go back")
    selection = input()

    if selection == "1": CLIPrintAllComputers()
    elif selection == "2": CLIPrintComputerBySearch()
    elif selection == "3": breakLoop = True

def CLIPrintAllComputers():
  computers = getComputers()
  computers = CallAdminAPI("get", "adminRoutes/adminComputers/get_computers", settings.adminToken)
  public = "Not public"
  for computer in computers:
    if computer["public"]:
      public = "Public"
    else: public = "Not public"
    print("id:", computer["computerId"], "-", public, "- name:", computer["name"], "- created at:", computer["createdAt"], "- updated at:", computer["updatedAt"])

def CLIPrintComputerBySearch():
  print("\nWhat is the id or name of the computer you are looking for? (name is case-sensitive)")
  filter = input()
  computers = CallAdminAPI("get", "adminRoutes/adminComputers/get_computers", settings.adminToken, params={"filter": filter})
  if computers != None:
    for computer in computers:
      if computer["public"]:
        public = "Public"
      else: public = "Not public"
      print("id:", computer["computerId"], "-", public, "- name:", computer["name"], "- created at:", computer["createdAt"], "- updated at:", computer["updatedAt"])
  else: print("No match found for:", filter)

def CLIaddComputer():
  breakLoop = False
  while breakLoop == False:
    print("\nComputer Adding")
    print("1) Add computer(s)")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"): CLIAddComputers()
    elif (selection == "2"): breakLoop = True

def CLIAddComputers():
  errors = 0
  print("\nList all the computers you want to add separated by commas: (Computer1,Computer2,Computer3,etc...)")

  computersToAdd = input().split(",")
  for computer in computersToAdd:
    print('\nIs "' + computer + '" public or not? (True / False)')
    public = input()
    if public.capitalize() == "True":
      public = True
    elif public.capitalize() == "False":
      public = False
    else:
      print("\nNot a valid value for publicity, only accepted values are: True or False")
      errors += 1
      continue
    result = CallAdminAPI("get", "adminRoutes/adminComputers/add_computer", settings.adminToken, params={"name": computer, "public": public})
    if result == None: 
      print("Couldn't add:", computer, "to computers, this name is already in use.")
      errors += 1
  print(len(computersToAdd)-errors, "computers were added to the database.") #Count of items that arent None

def CLIremoveComputer():
  breakLoop = False
  while breakLoop == False:
    print("\nComputer Removal")
    print("1) Remove computer")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"):
      print("\nWhat is the id or name of the computer you want to delete? (name is case-sensitive)")
      filter = input()
      computer = CallAdminAPI("get", "adminRoutes/adminComputers/get_computers", settings.adminToken, params={"filter": filter})
      if computer != None:
        computer = computer[0]
        CallAdminAPI("get", "adminRoutes/adminComputers/remove_computer", settings.adminToken, params={"computer_id": computer["computerId"]})
        print("Computer successfully removed.")
      else: print("No match found for:", filter)
    elif (selection == "2"): breakLoop = True

def CLIeditComputer():
  breakLoop = False
  while breakLoop == False:
    print("\nComputer Editing")
    print("1) Edit computer")
    print("2) Go back")
    selection = input()

    if (selection == "1"):
      print("\nWhat is the id or name of the computer you want to edit? (name is case-sensitive)")
      filter = input()
      computer = CallAdminAPI("get", "adminRoutes/adminComputers/get_computers", settings.adminToken, params={"filter": filter})
      if computer != None:
        computer = computer[0]
        CLIEditComputers(computer)
      else: print("No match found for:", filter)
    elif (selection == "2"): breakLoop = True

def CLIEditComputers(computer):
  breakLoop = False
  while breakLoop == False:
    print("\nWhich part of", computer["name"], "do you want to edit?")
    print("1) Edit name")
    print("2) Edit publicity")
    print("3) Edit all of the above")
    print("4) Go back")
    selection = input()
    if (selection == "1"):
        print("\nWhat do you want to edit " + computer["name"] + "'s name to?")
        new_name = input()
        params={"computer_id": computer["computerId"], "new_name": new_name}
        CallAdminAPI("get", "adminRoutes/adminComputers/edit_computer", settings.adminToken, params=params)
        print("Computer successfully edited.")
    elif (selection == "2"):
        print("\nWhat do you want to edit " + computer["name"] + "'s publicity to? (True/False)")
        new_public = input()
        if new_public.capitalize() == "True":
          new_public = True
        elif new_public.capitalize() == "False":
          new_public = False
        else:
          print("\nNot a valid value for publicity, only accepted values are: True or False") 
          continue
        params={"computer_id": computer["computerId"], "new_public": new_public}
        CallAdminAPI("get", "adminRoutes/adminComputers/edit_computer", settings.adminToken, params=params)
        print("Computer successfully edited.")
    elif (selection == "3"):
        print("\nWhat do you want to edit " + computer["name"] + "'s name to?")
        new_name = input()
        print("\nWhat do you want to edit " + computer["name"] + "'s publicity to? (True/False)")
        new_public = input()
        if new_public.capitalize() == "True":
          new_public = True
        elif new_public.capitalize() == "False":
          new_public = False
        else:
          print("\nNot a valid value for publicity, only accepted values are: True or False") 
          continue
        params={"computer_id": computer["computerId"], "new_name": new_name, "new_public": new_public}
        CallAdminAPI("get", "adminRoutes/adminComputers/edit_computer", settings.adminToken, params=params)
        print("Computer successfully edited.")
    elif (selection == "4"): breakLoop = True