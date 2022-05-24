def CLIuserstorages():
  breakLoop = False
  while breakLoop == False:
    print("\nManaging user storages (3 storages in database)")
    print("Type user email address or userId to first find user, or type exit to go back:")
    selection = input()

    if (selection == "exit"): breakLoop = True