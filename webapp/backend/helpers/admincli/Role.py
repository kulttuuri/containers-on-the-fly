from helpers.tables.Role import *

def CLIroles():
  breakLoop = False
  while breakLoop == False:
    print("\nManaging roles  (? roles in database)")
    print("What do you want to do?")
    print("1) List roles")
    print("2) Add new role")
    print("3) Remove role")
    print("4) Edit role")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIrolesList()
    elif (selection == "2"): CLIaddRole()
    elif (selection == "3"): CLIremoveRole()
    elif (selection == "4"): CLIeditRole()
    elif (selection == "5"): breakLoop = True

def CLIrolesList():
  breakLoop = False
  while breakLoop == False:
    print("\nRole Listing")
    print("1) List all roles")
    print("2) List roles by search")
    print("3) Go back")
    selection = input()
    
    if (selection == "1"): CLIPrintAllRoles()
    elif (selection == "2"): CLIPrintRolesBySearch()
    elif (selection == "3"): breakLoop = True

def CLIaddRole():
  breakLoop = False
  while breakLoop == False:
    print("\nRole Adding")
    print("1) Add role(s)")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"): CLIAddRoles()
    elif (selection == "2"): breakLoop = True

def CLIAddRoles():
  duplicates = 0
  print("\nList all the roles you want to add separated by commas: (Role1, Role2, Role3, etc...)")
  rolesToAdd = input().split(", ")
  for role in rolesToAdd:
    result = addRole(role)
    if result == None: 
      print("Couldn't add:", role, "to roles, this name is already in use.")
      duplicates = duplicates+1
  print(len(rolesToAdd)-duplicates, "roles were added to the database.") #Count of items that arent None

def CLIPrintAllRoles():
  roles = getRoles()
  print(roles)
  for role in roles:
    print("id:", role.roleId, "- name:", role.name, "- created at:", role.createdAt, "- updated at:", role.updatedAt)

def CLIPrintRolesBySearch():
  print("\nWhat is the name of the role you are looking for? (case-sensitive)")
  filter = input()
  roles = getRoles(filter) #a bit hardcoded perhaps
  print(roles)
  if roles != None:
    for role in roles:
        print("id:", role.roleId, "- name:", role.name, "- created at:", role.createdAt, "- updated at:", role.updatedAt)
  else: print("No match found for:", filter)

def CLIremoveRole():
  breakLoop = False
  while breakLoop == False:
    print("\nRole Removal")
    print("1) Remove role")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"):
      print("\nWhat is the name of the role you want to delete? (case-sensitive)")
      name = input()
      role = getRoles(name)
      if role != None:
        role = role[0]
        removeRole(role)
        print("Role successfully removed.")
      else: print("No match found for:", name)
    elif (selection == "2"): breakLoop = True

def CLIeditRole():
  breakLoop = False
  while breakLoop == False:
    print("\nRole Editing")
    print("1) Edit role")
    print("2) Go back")
    selection = input()

    if (selection == "1"):
      print("\nWhat is the name of the role you want to edit? (case-sensitive)")
      name = input()
      role = getRoles(name)
      if role != None:
        role = role[0]
        print("\nWhat do you want to edit", role.name, "to?")
        new_name = input()
        editRole(role, new_name)
        print("Role successfully edited.")
      else: print("No match found for:", name)
    elif (selection == "2"): breakLoop = True