def CLIuserwhitelisting():
  breakLoop = False
  while breakLoop == False:
    print("\nWhitelisting (3 users whitelisted in database)")
    print("1) View all users in the whitelist")
    print("2) Add user to whitelist")
    print("3) Remove user from whitelist")
    print("4) Go back")
    selection = input()

    if (selection == "4"): breakLoop = True