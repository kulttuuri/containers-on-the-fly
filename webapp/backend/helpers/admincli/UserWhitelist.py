from helpers.server import *
from settings import settings

def CLIuserwhitelisting():
  breakLoop = False
  while breakLoop == False: 
    print(f'\nWhitelisting ({len(CallAdminAPI("get", "adminRoutes/adminUserWhitelists/view_all", settings.adminToken)) } users whitelisted in database)')
    print("What do you want to do?")
    print("1) View all users in the whitelist")
    print("2) Add user to whitelist")
    print("3) Remove user from whitelist")
    print("4) Go back")
    selection = input()

    if (selection == "1"): CLIviewAll()
    elif (selection == "2"): CLIaddToWhitelist()
    elif (selection == "3"): CLIremoveFromWhitelist()
    elif (selection == "4"): breakLoop = True


def CLIviewAll():
  whitelisted_users = CallAdminAPI("get", "adminRoutes/adminUserWhitelists/view_all", settings.adminToken)
  print("\nCurrent emails in whitelist:")
  for user in whitelisted_users:
    print("id:", user["userWhitelistId"], "- email:", user["email"])


def CLIaddToWhitelist():
  print("\nList all the emails you want to whitelist separated by commas: (Email1, Email2, Email3, etc...)")
  emails = input().split(", ")
  duplicates = 0
  for email in emails:
    result = CallAdminAPI("get", "adminRoutes/adminUserWhitelists/add_to_whitelist", settings.adminToken, params= {"email": email})
    if result == None: 
      print("Couldn't whitelist " + email + ". Already whitelisted.")
      duplicates = duplicates+1
  print(len(emails)-duplicates, "emails were whitelisted.")


def CLIremoveFromWhitelist():
  print("\nList all the emails you want to unwhitelist separated by commas: (Email1, Email2, Email3, etc...)")
  emails_to_remove = input().split(", ")
  fails = 0
  for email in emails_to_remove:
    result = CallAdminAPI("get", "adminRoutes/adminUserWhitelists/remove_from_whitelist", settings.adminToken, params={"email": email})
    if result == None: 
      print("Failed to unwhitelist " + email + ". Not whitelisted.")
      fails = fails+1
  print(len(emails_to_remove)-fails, "emails were unwhitelisted.")
