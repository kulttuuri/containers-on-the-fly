from helpers.tables.Role import *
from helpers.server import *
from settings import settings

def CLIroles():
  breakLoop = False
  while breakLoop == False:
    print(f'\nManaging roles  ({len(CallAdminAPI("get", "adminRoutes/adminRoles/get_roles", settings.adminToken))} roles in database)')
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

def CLIPrintAllRoles():
  roles = CallAdminAPI("get", "adminRoutes/adminRoles/get_roles", settings.adminToken)
  for role in roles:
    print("id:", role["roleId"], "- name:", role["name"], "- created at:", role["createdAt"], "- updated at:", role["updatedAt"])

def CLIPrintRolesBySearch():
  print("\nWhat is the id or name of the role you are looking for? (name is case-sensitive)")
  filter = input()
  roles = CallAdminAPI("get", "adminRoutes/adminRoles/get_roles", settings.adminToken, params={"filter": filter})
  if roles != None:
    for role in roles:
      print("id:", role["roleId"], "- name:", role["name"], "- created at:", role["createdAt"], "- updated at:", role["updatedAt"])
  else: print("No match found for search:", filter)

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
    result = CallAdminAPI("get", "adminRoutes/adminRoles/add_role", settings.adminToken, params={"name": role})
    if result == None: 
      print("Couldn't add:", role, "to roles, this name is already in use.")
      duplicates = duplicates+1
  print(len(rolesToAdd)-duplicates, "roles were added to the database.") #Count of items that arent None

def CLIremoveRole():
  breakLoop = False
  while breakLoop == False:
    print("\nRole Removal")
    print("1) Remove role")
    print("2) Go back")
    selection = input()
    
    if (selection == "1"):
      print("\nWhat is the id or name of the role you want to delete? (name is case-sensitive)")
      filter = input()
      role = CallAdminAPI("get", "adminRoutes/adminRoles/get_roles", settings.adminToken, params={"filter": filter})
      if role != None:
        role = role[0]
        CallAdminAPI("get", "adminRoutes/adminRoles/remove_role", settings.adminToken, params={"role_id": role["roleId"]})
        print("Role successfully removed.")
      else: print("No match found for:", filter)
    elif (selection == "2"): breakLoop = True

def CLIeditRole():
  breakLoop = False
  while breakLoop == False:
    print("\nRole Editing")
    print("1) Edit role")
    print("2) Go back")
    selection = input()

    if (selection == "1"):
      print("\nWhat is the id or name of the role you want to edit? (name is case-sensitive)")
      filter = input()
      role = CallAdminAPI("get", "adminRoutes/adminRoles/get_roles", settings.adminToken, params={"filter": filter})
      if role != None:
        role = role[0]
        print("\nWhat do you want to edit " + role["name"] + "'s name to?")
        new_name = input()
        CallAdminAPI("get", "adminRoutes/adminRoles/edit_role", settings.adminToken, params={"role_id": role["roleId"], "new_name": new_name})
        print("Role successfully edited.")
      else: print("No match found for:", filter)
    elif (selection == "2"): breakLoop = True