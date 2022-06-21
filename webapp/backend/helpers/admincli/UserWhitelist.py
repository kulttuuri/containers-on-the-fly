from helpers.tables.UserWhitelist import *

def CLIuserwhitelisting():
  breakLoop = False
  count = CLIcountUsers()
  while breakLoop == False:
    print(f"\nWhitelisting ({count} users whitelisted in database)")
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
  for user in whitelisted_users:
    print(user.email)


def CLIaddToWhitelist():
  emails_to_input = input("Enter the users email that you want to whitelist. If you want to add several, divide them with ',' : ").split(",")
  for emails in emails_to_input:
    print(emails)  
  addToWhitelist(emails_to_input, emails)


def CLIremoveFromWhitelist():
  emails_to_remove = input("Enter the email address that you want to be removed from whitelist. If you want to remove several, divide them with ',' : ").split(",")
  for emails in emails_to_remove:
    print(emails)
  removeFromWhitelist(emails_to_remove, emails)


def CLIcountUsers():
  count = 0
  users = viewAll()
  for user in users:
    count+=1
  return count