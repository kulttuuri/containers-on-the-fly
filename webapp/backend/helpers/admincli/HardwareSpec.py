from helpers.tables.HardwareSpec import *
from helpers.tables.Computer import *

def CLIhardwarespecs():
  breakLoop = False
  while breakLoop == False:
    print(f"\nManaging hardwarespecs  ({len(getHardwarespecs())} hardwarespecs in database)")
    print("What do you want to do?")
    print("1) List hardwarespecs")
    print("2) Add new hardwarespec")
    print("3) Remove hardwarespec")
    print("4) Edit hardwarespec")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIhardwarespecsList()
    elif (selection == "2"): CLIaddHardwarespec()
    elif (selection == "3"): CLIremoveHardwarespec()
    elif (selection == "4"): CLIeditHardwarespec()
    elif (selection == "5"): breakLoop = True

def CLIhardwarespecsList():
  breakLoop = False
  while breakLoop == False:
    print("\nHardwarespec Listing")
    print("1) List all hardwarespecs")
    print("2) Go back")
    selection = input()

    if selection == "1": CLIPrintAllHardwarespecs()
    elif selection == "2": breakLoop = True

def CLIPrintAllHardwarespecs():
  hardwarespecs = getHardwarespecs()
  for hardwarespec in hardwarespecs:
    print("id:", hardwarespec.hardwareSpecId, "- computer id:", hardwarespec.computerId, "- type:", hardwarespec.type)
    print("max amount:", hardwarespec.maximumAmount, "- min amount:", hardwarespec.minimumAmount)
    print("max amount for user:", hardwarespec.maximumAmountForUser, "- default amount for user:", hardwarespec.defaultAmountForUser)
    print("format:", hardwarespec.format,"- created at:", hardwarespec.createdAt, "- updated at:", hardwarespec.updatedAt)

def CLIaddHardwarespec():
  breakLoop = False
  while breakLoop == False:
    print("\nHardwarespec Adding")
    print("1) Add a hardwarespec")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"): CLIAddHardwarespecs()
    elif (selection == "2"): breakLoop = True

def CLIAddHardwarespecs():
  print("\nWhat computer id or name should be associated with this hardware? (name is case-sensitive)")
  filter = input()
  doesComputerExist = getComputers(filter)
  if doesComputerExist == None: 
    print("No computer found with that search, exiting creation...")
    return
  else: computerId = doesComputerExist[0].computerId
  print("\nWhat type of hardware is this?")
  type = input()
  print("\nWhat is the maximum amount for this hardware?")
  maxAmount = input()
  try: maxAmount = int(maxAmount)
  except:
    print("Error. Not a number, exiting...")
    return
  print("\nWhat is the minimum amount for this hardware?")
  minAmount = input()
  try: minAmount = int(minAmount)
  except:
    print("Error. Not a number, exiting...")
    return
  print("\nWhat is the maximum amount for a user?")
  maxUserAmount = input()
  try: maxUserAmount = int(maxUserAmount)
  except:
    print("Error. Not a number, exiting...")
    return
  print("\nWhat is the default amount for a user?")
  defaultUserAmount = input()
  try: defaultUserAmount = int(defaultUserAmount)
  except:
    print("Error. Not a number, exiting...")
    return
  print("\nWhat is the format of this hardware?")
  format = input()
  addHardwarespec(computerId, type, maxAmount, minAmount, maxUserAmount, defaultUserAmount, format)
  print("New hardwarespec was added to the database.")

def CLIremoveHardwarespec():
  breakLoop = False
  while breakLoop == False:
    print("\nHardwarespec Removal")
    print("1) Remove hardwarespec")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"):
      print("\nWhat is the id of the hardwarespec you want to delete?")
      id = input()
      hardwarespec = getHardwarespecs(id)
      if hardwarespec != None:
        hardwarespec = hardwarespec[0]
        removeHardwarespec(hardwarespec)
        print("Hardwarespec successfully removed.")
      else: print("No match found for id:", id)
    elif (selection == "2"): breakLoop = True

def CLIeditHardwarespec():
  breakLoop = False
  while breakLoop == False:
    print("\nHardwarespec Editing")
    print("1) Edit hardwarespec")
    print("2) Go back")
    selection = input()

    if (selection == "1"):
      print("\nWhat is the id of the hardwarespec you want to edit?")
      id = input()
      hardwarespec = getHardwarespecs(id)
      if hardwarespec != None:
        hardwarespec = hardwarespec[0]
        CLIEditHardwarespecs(hardwarespec)
      else: print("No match found for id:", id)
    elif (selection == "2"): breakLoop = True

def CLIEditHardwarespecs(hardwarespec):
  breakLoop = False
  while breakLoop == False:
    print("\nYou are currently editing harwarespec with id ", hardwarespec.hardwareSpecId)
    print("1) Edit all fields, leave question field empty to not change field")
    print("2) Go back")
    selection = input()
    if (selection == "1"):
      print("\nWhat computer (id or name) should be associated with this hardware? Current value:", )
      new_computer = input()
      if new_computer != "":
        doesComputerExist = getComputers(new_computer)
        if doesComputerExist == None: 
          print("No computer found with search, defaulting to old value")
          new_computer = None
        else: new_computer = doesComputerExist[0].computerId
      else: new_computer = None
      print("\nWhat type of hardware is this?")
      new_type = input()
      if new_type == "":
        new_type = None
      print("\nWhat is the maximum amount for this hardware?")
      new_max = input()
      if new_max != "":
        try: new_max = int(new_max)
        except:
          print("Error. Not a number, defaulting to old value")
          new_max = None
      else: new_max = None
      print("\nWhat is the minimum amount for this hardware?")
      new_min = input()
      if new_min != "":
        try: new_min = int(new_min)
        except:
          print("Error. Not a number, defaulting to old value")
          new_min = None
      else: new_min = None
      print("\nWhat is the maximum amount for a user?")
      new_user_max = input()
      if new_user_max != "":
        try: new_user_max = int(new_user_max)
        except:
          print("Error. Not a number, defaulting to old value")
          new_user_max = None
      else: new_user_max = None
      print("\nWhat is the default amount for a user?")
      new_default = input()
      if new_default != "":
        try: new_default = int(new_default)
        except:
          print("Error. Not a number, defaulting to old value")
          new_default = None
      else: new_default = None
      print("\nWhat is the format of this hardware?")
      new_format = input()
      if new_format == "":
        new_format = None
      try: 
        editHardwarespec(hardwarespec, new_computer, new_type, new_max, new_min, new_user_max, new_default, new_format)
        print("Hardwarespec successfully edited.")
      except:
        print("Something failed while editing this hardware")
    elif (selection == "2"): breakLoop = True
