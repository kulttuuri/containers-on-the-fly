from database import ReservedContainer
from helpers.tables.Reservation import *
from helpers.tables.Computer import *
from helpers.tables.Container import *
from helpers.tables.User import *
from datetime import datetime
from datetime import timedelta

def CLIreservations():
  breakloop = False
  reserved_count  = CLIcount("reserved")
  started_count = CLIcount("started")
  stopped_count = CLIcount("stopped")
  while breakloop == False:
    print(f"\nManaging reservations ( {reserved_count} reserved, {started_count} started, {stopped_count} stopped reservation(s) in database)")
    print("What do you want to do?")
    print("1) List all reservations")
    print("2) Add reservation")
    print("3) Remove reservation")
    print("4) Edit reservation")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIreservationsList()
    if (selection == "2"): CLIaddReservation()
    if (selection == "3"): CLIremoveReservation()
    if (selection == "4"): CLIeditReservation()
    elif (selection == "5"): breakloop = True


def CLIreservationsList():
  breakloop = False
  while breakloop == False:
    print("\nReservation listing")
    print("1) List all reservations")
    print("2) List reservations by search")
    print("3) Go back")
    selection = input()

    if selection == "1": CLIPrintAllReservations()
    elif selection == "2": CLIPrintReservationsBySearch()
    elif selection == "3": CLIreservations()


def CLIPrintAllReservations():
  print("\nList of all the reservations:")
  reservations = getReservations()
  if reservations != None:
    for reservation in reservations:
      print("id:", reservation.reservationId, " containerId:", reservation.reservedContainerId, " computerId:", reservation.computerId,
      "- userId:", reservation.userId, "- startDate:", reservation.startDate, "- endDate:", reservation.endDate, "- createdAt:", reservation.createdAt, "- updatedAt:", reservation.updatedAt, "- status:", reservation.status)
  else:
    print("There are no reservations.")


def CLIPrintReservationsBySearch():
  print("\nSearch for a specific reservation. Do you want to search by startDate, endDate or status?")
  List_by = input()
  
  if List_by == "startDate":
    print("\nWhat is the startDate you are trying to search for? Format: Day-Month-Year Hour:Minute:Second")
    startDate = input()
    try:
      startDate = datetime.strptime(startDate, '%d-%m-%y %H:%M:%S')
      reservations = getReservations(startDate)
      if reservations != None:
        print("\nReservation(s) found with that date:")
        for reservation in reservations:
          print("id:", reservation.reservationId, "- containerId:", reservation.reservedContainerId, "- computerId:", reservation.computerId,
         "- userId:", reservation.userId, "- startDate:", reservation.startDate, "- endDate:", reservation.endDate, "- createdAt:", reservation.createdAt, "- updatedAt:", reservation.updatedAt, "- status:", reservation.status)
      else:
       print("\nNo reservation found for that date.")
    except ValueError:
      print("Date you tried to enter was not in the correct format! Example: 12-07-22 13:00:00")
  
  elif List_by == "endDate":
    print("\nWhat is the endDate you are trying to search for? Format: Day-Month-Year Hour:Minute:Second")
    endDate = input()
    try:
      endDate = datetime.strptime(endDate, '%d-%m-%y %H:%M:%S')
      reservations = getReservations(endDate)
      if reservations != None:
        print("\nReservation(s) found with that date:")
        for reservation in reservations:
          print("id:", reservation.reservationId, "- containerId:", reservation.reservedContainerId, "- computerId:", reservation.computerId,
         "- userId:", reservation.userId, "- startDate:", reservation.startDate, "- endDate:", reservation.endDate, "- createdAt:", reservation.createdAt, "- updatedAt:", reservation.updatedAt, "- status:", reservation.status)
      else:
       print("\nNo reservation found for that date.")
    except ValueError:
      print("Date you tried to enter was not in the correct format! Example: 12-07-22 13:00:00")
  
  elif List_by == "status":
    print("\nWhat is the status of the reservation you are trying to search? Options: reserved, started, stopped")
    status = input()
    reservations = getReservations(status)
    if reservations != None:
      print("\nReservation(s) found with that status:")
      for reservation in reservations:
        print("id:", reservation.reservationId, "- containerId:", reservation.reservedContainerId, "- computerId:", reservation.computerId,
        "- userId:", reservation.userId, "- startDate:", reservation.startDate, "- endDate:", reservation.endDate, "- createdAt:", reservation.createdAt, "- updatedAt:", reservation.updatedAt, "- status:", reservation.status)
    else:
      print("\nNo reservation found for that status.")  
  
  elif List_by == "":
    reservations = getReservations()
    if reservations != None:
      print("\nList of reservation(s):")
      for reservation in reservations:
        print("id:", reservation.reservationId, "- containerId:", reservation.reservedContainerId, "- computerId:", reservation.computerId,
        "- userId:", reservation.userId, "- startDate:", reservation.startDate, "- endDate:", reservation.endDate, "- createdAt:", reservation.createdAt, "- updatedAt:", reservation.updatedAt, "- status:", reservation.status)
    else:
      print("There are no reservations.")
  else:  
    print("Input was incorrect. Enter one of these: startDate, endDate, status")


def CLIaddReservation():
  breakloop = False
  while breakloop == False:
    print("\nAdding reservation")
    print("1) Add reservation(s)")
    print("2) Go back")
    selection = input()

    if (selection == "1"): CLIaddReservations()
    elif (selection == "2"): CLIreservations()

def CLIaddReservations():
  print("\nID or email of the user making the reservation:")
  filter = input()
  doesUserExist = getUser(filter)
  if doesUserExist == None:
    print("No user with that id, exiting creation...")
    return
  else: userId = doesUserExist.userId
  
  print("\nEnter the computer name or id that you want to be associated with this reservation.")
  computerName = input()
  doesComputerExist = getComputers(computerName)
  if doesComputerExist != None:
    computerName = doesComputerExist[0].computerId
    print("\nYou chose", computerName, "from the list below.")
    all_computers = getComputers()
    for computer in all_computers:
      print("id:", computer.computerId, "name:", computer.name)
  else:
      print("No computer with that id, exiting creation...")
      all_computers = getComputers()
      print("\nChoose one of the computers below:")
      for computer in all_computers:
        print("id:", computer.computerId, "name:", computer.name)
      return
  
  print("\nEnter the container name or id that you want to be associated with this reservation.")
  containerName = input()
  doesContainerExist = getContainers(containerName)
  if doesContainerExist != None:
    container = doesContainerExist[0].containerId
    print("\nYou chose", containerName, "from the list below.")
    all_containers = getContainers()
    for containers in all_containers:
      print("id:", containers.containerId, "name:", containers.name) 
  else:
      print("No container with that id, exiting creation...")
      all_containers = getContainers()
      print("\nChoose one of the containers below:")
      for containers in all_containers:
        print("id:", containers.containerId, "name:", containers.name)
      return

  print("\nEnter start date of your reservation. Make sure date format is 'Day-Month-Year Hour:Minute:Second'. Please enter date as UTC+0: ")
  print("Leave start date empty if you want to set it as now:")
  startDate = input()
  print("\nEnter end date of your reservation. Make sure date format is 'Day-Month-Year Hour:Minute:Second'. Please enter date as UTC+0.")
  print("Leave end date empty to set it +4 hours from start date:")
  endDate = input()
  if startDate == "":
    startDate = datetime.now()
    startDate = startDate.strftime('%d-%m-%y %H:%M:%S')
  if endDate == "":
    current_date = datetime.strptime(startDate, '%d-%m-%y %H:%M:%S')
    n = 4
    endDate = current_date + timedelta(hours = n)
    endDate = endDate.strftime('%d-%m-%y %H:%M:%S')
  try: 
      startDate = datetime.strptime(startDate, '%d-%m-%y %H:%M:%S')
      endDate = datetime.strptime(endDate, '%d-%m-%y %H:%M:%S')
      print("\nReservation was added succesfully! Start date:", startDate, "- End date:", endDate)
      addReservation(startDate, endDate, userId, computerName, container)
  except ValueError:
    print("Date you tried to enter was not in the correct format! Example: 12-07-22 13:00:00")
    

def CLIremoveReservation():
  breakloop = False
  while breakloop == False:
    print("\nRemoving reservations:")
    print("1) Remove reservation")
    print("2) Go back")
    selection = input()

    if (selection == "1"):
      print("\nType the id of the reservation that you want to remove:")
      reservationId = int(input())
      reservation = getReservation(reservationId)
      if reservation != None:
        reservation = reservation[0]
        removeReservation(reservation)
        print("Reservation was removed succesfully.")
      else:
        print("No reservation found for:", reservationId)
    elif (selection == "2"):
      CLIreservations()
    

def CLIeditReservation():
  breakloop = False
  while breakloop == False:
    print("\nEditing reservations:")
    print("1) Edit reservation")
    print("2) Go back")
    selection = input()

    if (selection == "1"):
      print("\nWhat is the id of the reservation you want to edit?")
      reservationId = int(input())
      reservations = getReservation(reservationId)
      if reservations != None:
        reservations = reservations[0]
        print("Reservation found for:", reservationId)
        CLIeditReservations(reservations)
      else:
        print("No reservation found for id:", reservationId)
    elif (selection == "2"):
      CLIreservations()

def CLIeditReservations(reservation):
  breakloop = False
  while breakloop == False:
    print("\nWhich part of the reservation would you like to edit?")
    print("1) Edit startDate")
    print("2) Edit endDate")
    print("3) Edit status")
    print("4) Edit all of the above")
    print("5) Go back")
    selection = input()
    
    if (selection == "1"):
      print("\nWhat date do you want to edit current start date of", reservation.startDate,"to? Format: Day-Month-Year Hour:Minute:Second") 
      new_startDate = input()
      try:
        new_startDate = datetime.strptime(new_startDate, '%d-%m-%y %H:%M:%S')
        editReservation(reservation, new_startDate, None)
        print("Reservation start date edited successfully. New start date:", new_startDate)
      except ValueError:
        print("Date you tried to enter was not in the correct format. Example: 12-07-22 13:00:00")
        continue
     
    elif (selection == "2"):
      print("\nWhat date do you want to edit current end date of", reservation.endDate,"to? Format: Day-Month-Year Hour:Minute:Second")
      new_endDate = input()
      try:
        new_endDate = datetime.strptime(new_endDate, '%d-%m-%y %H:%M:%S')
        editReservation(reservation, None, new_endDate)
        print("Reservation end date edited succesfully. New end date:", new_endDate)
      except ValueError:
        print("Date you tried to enter was not in the correct format. Example: 12-07-22 13:00:00")
        continue
    
    
    elif (selection == "3"):
      print("\nReservations current status is", reservation.status,". What do you want to change it to? Choose either: reserved, started, stopped.")
      new_status = input()
      if new_status == "reserved":
        status = new_status
        print("Status changed succesfully.")
        editReservation(reservation, None, None, new_status)
      elif new_status == "started":
        status = new_status
        print("Status changed succesfully.")
        editReservation(reservation, None, None, new_status)
      elif new_status == "stopped":
        status = new_status
        print("Status changed succesfully.")
        editReservation(reservation, None, None, new_status)
      else:
        print("\nNot a valid value for status. Choose either reserved, started or stopped.")
        continue
      
    elif (selection == "4"):
      print("\nWhat date do you want to edit current start date of", reservation.startDate,"to? Format: Day-Month-Year Hour:Minute:Second")
      new_startDate = input()
      try:
        new_startDate = datetime.strptime(new_startDate, '%d-%m-%y %H:%M:%S')
        print("Reservation start date edited successfully.")
      except ValueError:
        print("Date you tried to enter was not in the correct format. Example: 12-07-22 13:00:00")
        continue
      
      print("\nWhat date do you want to edit current end date of", reservation.endDate,"to? Format: Day-Month-Year Hour:Minute:Second")
      new_endDate = input()
      try:
        new_endDate = datetime.strptime(new_endDate, '%d-%m-%y %H:%M:%S')
        print("Reservation end date edited succesfully.")
      except ValueError:
        print("Date you tried to enter was not in the correct format. Example: 12-07-22 13:00:00")
        continue
      
      print("\nReservations current status is", reservation.status,". What do you want to change it to? Choose either: reserved, started, stopped.")
      new_status = input()
      if new_status == "reserved":
        status = new_status
        editReservation(reservation, new_startDate, new_endDate, status)
        print("Reservation edited succesfully. Current reservation: - StartDate:", reservation.startDate," - EndDate:", reservation.endDate," - Status:", reservation.status)
      elif new_status == "started":
        status = new_status
        editReservation(reservation, new_startDate, new_endDate, status)
        print("Reservation edited succesfully. Current reservation: - StartDate:", reservation.startDate," - EndDate:", reservation.endDate," - Status:", reservation.status)
      elif new_status == "stopped":
        status = new_status
        editReservation(reservation, new_startDate, new_endDate, status)
        print("Reservation edited succesfully. Current reservation: - StartDate:", reservation.startDate," - EndDate:", reservation.endDate," - Status:", reservation.status)
      else:
        print("\nNot a valid value for status. Choose either reserved, started or stopped.")
        continue
      
    elif (selection == "5"): CLIreservations()


def CLIcount(filterby):
  reserved_count = 0
  reservations = getReservations(filterby)
  try:
    for reservation in reservations:
      reserved_count+=1
    return reserved_count
  except TypeError:
    reserved_count
  