from helpers.tables.UserWhitelist import *
from helpers.tables.User import *

def CLIuserwhitelisting():
  breakLoop = False
  while breakLoop == False:
    print(f"\nWhitelisting ({len(viewAll())} users whitelisted in database)")
    print("1) View all users in the whitelist")
    print("2) Add user to whitelist")
    print("3) Remove user from whitelist")
    print("4) Go back")
    selection = input()
    print("")

    if (selection == "1"): CLIviewAll()
    elif (selection == "2"): CLIaddToWhitelist()
    elif (selection == "3"): CLIremoveFromWhitelist()
    elif (selection == "4"): breakLoop = True


def CLIviewAll():
  whitelisted_users = viewAll()
  print("Current emails in whitelist:")
  for user in whitelisted_users:
    print(user.email)


def CLIaddToWhitelist():
  emails_to_input = input("Enter the users email that you want to whitelist. If you want to add several, divide them with ',' and no space: ").split(",") 
  for emails in emails_to_input:
    doesEmailExist = getUser(emails)
    print("")
    print(emails)
    if doesEmailExist != None:
      try: 
        addToWhitelist(emails_to_input, emails)
      except:
        print()
    else:
      print("No user with that email.")



def CLIremoveFromWhitelist():
  emails_to_remove = input("Enter the email address that you want to be removed from whitelist. If you want to remove several, divide them with ',' and no space: ").split(",")
  for emails in emails_to_remove:
    doesEmailExist = viewAll(emails)
    print("")
    print(emails)
    if doesEmailExist != None:
      try:
        removeFromWhitelist(emails_to_remove, emails)
      except:
        print()
    else:
      print("No user with that email in whitelist.")