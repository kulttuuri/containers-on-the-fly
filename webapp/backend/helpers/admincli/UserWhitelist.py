from helpers.tables.UserWhitelist import *
from helpers.tables.User import *
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
  # The adding still doesn't really work I guess because of the API problem in the get_user
  emails_to_input = input("Enter the users email that you want to whitelist. If you want to add several, divide them with ',' and no space: ").split(",") 
  for emails in emails_to_input:
    does_email_exist = CallAdminAPI("get", "adminRoutes/adminUsers/get_user", settings.adminToken, params={"findby": emails})
    print("")
    print(emails)
    if does_email_exist != None:
      try: 
        CallAdminAPI("get", "adminRoutes/adminUserWhitelists/add_to_whitelist", settings.adminToken, params= {"emails_to_input": emails_to_input, "emails": emails})
        print("Email succesfully added.")
      except:
        print()
    elif does_email_exist == None:
      print("No user with that email.")


def CLIremoveFromWhitelist():
  emails_to_remove = input("Enter the email address that you want to be removed from whitelist. If you want to remove several, divide them with ',' and no space: ").split(",")
  for emails in emails_to_remove:
    does_email_exist = CallAdminAPI("get", "adminRoutes/adminUserWhitelists/view_all", settings.adminToken, params={"opt_filter": emails})
    print("")
    print(emails)
    if does_email_exist:
      try:
        CallAdminAPI("get", "adminRoutes/adminUserWhitelists/remove_from_whitelist", settings.adminToken, params={"emails_to_remove": emails_to_remove, "emails": emails})
        print("Email succesfully deleted.")
      except:
        print()
    else:
      print("No user with that email in whitelist.")

