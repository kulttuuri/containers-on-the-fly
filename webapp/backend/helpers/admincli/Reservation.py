def CLIreservations():
  breakLoop = False
  while breakLoop == False:
    print("\nManaging reservations (3 active, 3 future, 3 old reservations in database)")
    print("What do you want to do?")
    print("1) List all reservations")
    print("2) List all reservations")
    selection = input()

    if (selection == "3"): breakLoop = True