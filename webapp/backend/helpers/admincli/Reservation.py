from database import ReservedContainer
from helpers.tables.Reservation import *
from helpers.tables.Computer import *
from helpers.tables.Container import *
from helpers.tables.User import *
from helpers.server import *
from settings import settings
from datetime import datetime
from datetime import timedelta

def CLIreservations():
  breakloop = False
  while breakloop == False:
    reserved_count  = CLIcount("reserved")
    started_count = CLIcount("started")
    stopped_count = CLIcount("stopped")
    print(f"\nManaging reservations ( {reserved_count} reserved, {started_count} started, {stopped_count} stopped reservation(s) in database)")
    print("What do you want to do?")
    print("1) List all reservations")
    print("2) Add reservation")
    print("3) Remove reservation")
    print("4) Edit reservation")
    print("5) Go back")
    selection = input()

    if (selection == "1"): CLIreservationsList()
    elif (selection == "2"): CLIaddReservation()
    elif (selection == "3"): CLIremoveReservation()
    elif (selection == "4"): CLIeditReservation()
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
  reservations = CallAdminAPI("get", "adminRoutes/adminReservations/get_reservations", settings.adminToken)
  if reservations != None:
    for reservation in reservations:
      print("id:", reservation["reservationId"], "- containerId:", reservation["reservedContainerId"], "- computerId:", reservation["computerId"],
      "- userId:", reservation["userId"], "- startDate:", reservation["startDate"], "- endDate:", reservation["endDate"], "- createdAt:", reservation["createdAt"], "- updatedAt:", reservation["updatedAt"], "- status:", reservation["status"])
  else:
    print("There are no reservations.")


def CLIPrintReservationsBySearch():
  print("\nSearch for a specific reservation. Do you want to search by startDate, endDate or status?")
  List_by = input()
  
  if List_by == "startDate":
    print("\nWhat is the startDate you are trying to search for? (Format: Year-Month-Day Hour:Minute:Second ex.2022-07-08 12:00:00)")
    startDate = input()
    try:
      startDate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
      reservations = CallAdminAPI("get", "adminRoutes/adminReservations/get_reservations", settings.adminToken, params={"filter": startDate})
      if reservations != None:
        print("\nReservation(s) found with that date:")
        for reservation in reservations:
          print("id:", reservation["reservationId"], "- containerId:", reservation["reservedContainerId"], "- computerId:", reservation["computerId"],
         "- userId:", reservation["userId"], "- startDate:", reservation["startDate"], "- endDate:", reservation["endDate"], "- createdAt:", reservation["createdAt"], "- updatedAt:", reservation["updatedAt"], "- status:", reservation["status"])
      else:
       print("\nNo reservation found for that date.")
    except ValueError:
      print("Date you tried to enter was not in the correct format! Example: 2022-07-12 13:00:00")
  
  elif List_by == "endDate":
    print("\nWhat is the endDate you are trying to search for? (Format: Year-Month-Day Hour:Minute:Second ex.2022-07-08 12:00:00)")
    endDate = input()
    try:
      endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
      reservations = CallAdminAPI("get", "adminRoutes/adminReservations/get_reservations", settings.adminToken, params={"filter": endDate})
      if reservations != None:
        print("\nReservation(s) found with that date:")
        for reservation in reservations:
          print("id:", reservation["reservationId"], "- containerId:", reservation["reservedContainerId"], "- computerId:", reservation["computerId"],
          "- userId:", reservation["userId"], "- startDate:", reservation["startDate"], "- endDate:", reservation["endDate"], "- createdAt:", reservation["createdAt"], "- updatedAt:", reservation["updatedAt"], "- status:", reservation["status"])
      else:
        print("\nNo reservation found for that date.")
    except ValueError:
      print("Date you tried to enter was not in the correct format! Example: 2022-07-12 13:00:00")
  
  elif List_by == "status":
    print("\nWhat is the status of the reservation you are trying to search? Options: reserved, started, stopped")
    status = input()
    reservations = CallAdminAPI("get", "adminRoutes/adminReservations/get_reservations", settings.adminToken, params={"filter": status})
    if reservations != None:
      print("\nReservation(s) found with that status:")
      for reservation in reservations:
        print("id:", reservation["reservationId"], "- containerId:", reservation["reservedContainerId"], "- computerId:", reservation["computerId"],
        "- userId:", reservation["userId"], "- startDate:", reservation["startDate"], "- endDate:", reservation["endDate"], "- createdAt:", reservation["createdAt"], "- updatedAt:", reservation["updatedAt"], "- status:", reservation["status"])
    else:
      print("\nNo reservation found for that status.")  
  
  elif List_by == "":
    reservations = CallAdminAPI("get", "adminRoutes/adminReservations/get_reservations", settings.adminToken)
    if reservations != None:
      print("\nList of reservation(s):")
      for reservation in reservations:
        print("id:", reservation["reservationId"], "- containerId:", reservation["reservedContainerId"], "- computerId:", reservation["computerId"],
        "- userId:", reservation["userId"], "- startDate:", reservation["startDate"], "- endDate:", reservation["endDate"], "- createdAt:", reservation["createdAt"], "- updatedAt:", reservation["updatedAt"], "- status:", reservation["status"])
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
  # The get_user API problem occures here also
  print("\nID or email of the user making the reservation:")
  user = input()
  doesUserExist = CallAdminAPI("get", "adminRoutes/adminUsers/get_user", settings.adminToken, params={"findby": user})
  if doesUserExist != None:
    userId = doesUserExist["userId"]
  else:
    print("No user with that id, exiting creation...")
    return

  print("\nEnter the computer name or id that you want to be associated with this reservation.")
  computerName = input()
  doesComputerExist = CallAdminAPI("get", "adminRoutes/adminComputers/get_computers", settings.adminToken, params={"filter": computerName})
  if doesComputerExist != None:
    computerId = doesComputerExist[0]["computerId"]
    print("\nYou chose", computerName, "from the list below.")
    all_computers = CallAdminAPI("get", "adminRoutes/adminComputers/get_computers", settings.adminToken)
    for computer in all_computers:
      print("id:", computer["computerId"], "name:", computer["name"])
  else:
      print("No computer with that id, exiting creation...")
      all_computers = CallAdminAPI("get", "adminRoutes/adminComputers/get_computers", settings.adminToken)
      print("\nChoose one of the computers below:")
      for computer in all_computers:
        print("id:", computer["computerId"], "name:", computer["name"])
      return
  
  print("\nEnter the container name or id that you want to be associated with this reservation.")
  containerName = input()
  doesContainerExist = CallAdminAPI("get", "adminRoutes/adminContainers/get_containers", settings.adminToken, params={"filter": containerName})
  if doesContainerExist != None:
    containerId = doesContainerExist[0]["containerId"]
    print("\nYou chose", containerName, "from the list below.")
    all_containers = CallAdminAPI("get", "adminRoutes/adminContainers/get_containers", settings.adminToken)
    for containers in all_containers:
      print("id:", containers["containerId"], "name:", containers["name"]) 
  else:
      print("No container with that id, exiting creation...")
      all_containers = CallAdminAPI("get", "adminRoutes/adminContainers/get_containers", settings.adminToken)
      print("\nChoose one of the containers below:")
      for containers in all_containers:
        print("id:", containers["containerId"], "name:", containers["name"])
      return

  print("\nEnter start date of your reservation. Make sure date format is 'Year-Month-Day Hour:Minute:Second'(ex.2022-06-11 12:00:00). Please enter date as UTC+0.")
  print("Leave start date empty if you want to set it as now:")
  startDate = input()
  print("\nEnter end date of your reservation. Make sure date format is 'Year-Month-Day Hour:Minute:Second'(ex.2022-06-12 12:00:00). Please enter date as UTC+0.")
  print("Leave end date empty to set it +4 hours from start date:")
  endDate = input()
  if startDate == "":
    startDate = datetime.now()
    startDate = startDate.strftime('%Y-%m-%d %H:%M:%S')
  if endDate == "":
    current_date = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
    h = 4
    endDate = current_date + timedelta(hours = h)
    endDate = endDate.strftime('%Y-%m-%d %H:%M:%S')
  try: 
      startDate = datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
      endDate = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
      print("\nReservation was added succesfully! Start date:", startDate, "- End date:", endDate)
      params = {"startDate": startDate, "endDate": endDate, "userId": userId, "computerId": computerId, "containerId": containerId}
      CallAdminAPI("get", "adminRoutes/adminReservations/add_reservation", settings.adminToken, params=params)
  except ValueError:
    print("Date you tried to enter was not in the correct format! Example: 2022-07-12 13:00:00")
    

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
      reservation = CallAdminAPI("get", "adminRoutes/adminReservations/get_reservation", settings.adminToken, params={"filter": reservationId})
      if reservation != None:
        reservation = reservation[0]
        CallAdminAPI("get", "adminRoutes/adminReservations/remove_reservation", settings.adminToken, params={"reservation_id": reservation["reservationId"]})
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
      reservations = CallAdminAPI("get", "adminRoutes/adminReservations/get_reservation", settings.adminToken, params={"filter": reservationId})
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
      print("\nWhat date do you want to edit current start date of", reservation["startDate"],"to? (Format: Year-Month-Day Hour:Minute:Second ex.2022-07-08 12:00:00)") 
      new_startDate = input()
      try:
        new_startDate = datetime.strptime(new_startDate, '%Y-%m-%d %H:%M:%S')
        params = {"reservation_id": reservation["reservationId"], "new_startDate": new_startDate}
        CallAdminAPI("get", "adminRoutes/adminReservations/edit_reservation", settings.adminToken, params=params)
        print("Reservation start date edited successfully. New start date:", new_startDate)
      except ValueError:
        print("Date you tried to enter was not in the correct format. Example: 2022-07-12 13:00:00")
        continue
     
    elif (selection == "2"):
      print("\nWhat date do you want to edit current end date of", reservation["endDate"],"to? (Format: Year-Month-Day Hour:Minute:Second ex.2022-07-08 12:00:00)")
      new_endDate = input()
      try:
        new_endDate = datetime.strptime(new_endDate, '%Y-%m-%d %H:%M:%S')
        params = {"reservation_id": reservation["reservationId"], "new_endDate": new_endDate}
        CallAdminAPI("get", "adminRoutes/adminReservations/edit_reservation", settings.adminToken, params=params)
        print("Reservation end date edited succesfully. New end date:", new_endDate)
      except ValueError:
        print("Date you tried to enter was not in the correct format. Example: 2022-07-12 13:00:00")
        continue
    
    
    elif (selection == "3"):
      print("\nReservations current status is", reservation["status"],". What do you want to change it to? Choose either: reserved, started, stopped.")
      new_status = input()
      if new_status == "reserved":
        status = new_status
        params = {"reservation_id": reservation["reservationId"], "new_status": new_status}
        CallAdminAPI("get", "adminRoutes/adminReservations/edit_reservation", settings.adminToken, params=params)      
        print("Status changed succesfully.")      
      elif new_status == "started":
        status = new_status
        params = {"reservation_id": reservation["reservationId"], "new_status": new_status}
        CallAdminAPI("get", "adminRoutes/adminReservations/edit_reservation", settings.adminToken, params=params)
        print("Status changed succesfully.")
      elif new_status == "stopped":
        status = new_status
        params = {"reservation_id": reservation["reservationId"], "new_status": new_status}
        CallAdminAPI("get", "adminRoutes/adminReservations/edit_reservation", settings.adminToken, params=params)
        print("Status changed succesfully.")
      else:
        print("\nNot a valid value for status. Choose either reserved, started or stopped.")
        continue
      
    elif (selection == "4"):
      print("\nWhat date do you want to edit current start date of", reservation["startDate"],"to? (Format: Year-Month-Day Hour:Minute:Second ex.2022-07-08 12:00:00)")
      new_startDate = input()
      try:
        new_startDate = datetime.strptime(new_startDate, '%Y-%m-%d %H:%M:%S')
        print("Reservation start date edited successfully.")
      except ValueError:
        print("Date you tried to enter was not in the correct format. Example: 2022-07-12 13:00:00")
        continue
      
      print("\nWhat date do you want to edit current end date of", reservation["endDate"],"to? (Format: Year-Month-Day Hour:Minute:Second ex.2022-07-08 12:00:00)")
      new_endDate = input()
      try:
        new_endDate = datetime.strptime(new_endDate, '%Y-%m-%d %H:%M:%S')
        print("Reservation end date edited succesfully.")
      except ValueError:
        print("Date you tried to enter was not in the correct format. Example: 2022-07-12 13:00:00")
        continue
      
      print("\nReservations current status is", reservation["status"],". What do you want to change it to? Choose either: reserved, started, stopped.")
      new_status = input()
      if new_status == "reserved":
        status = new_status
        params = {"reservation_id": reservation["reservationId"], "new_startDate": new_startDate, "new_endDate": new_endDate, "new_status": new_status}
        CallAdminAPI("get", "adminRoutes/adminReservations/edit_reservation", settings.adminToken, params=params)
        print("Reservation edited succesfully. Current reservation: - StartDate:", new_startDate," - EndDate:", new_endDate," - Status:", new_status)
      elif new_status == "started":
        status = new_status
        params = {"reservation_id": reservation["reservationId"], "new_startDate": new_startDate, "new_endDate": new_endDate, "new_status": new_status}
        CallAdminAPI("get", "adminRoutes/adminReservations/edit_reservation", settings.adminToken, params=params)
        print("Reservation edited succesfully. Current reservation: - StartDate:", new_startDate," - EndDate:", new_endDate," - Status:", new_status)
      elif new_status == "stopped":
        status = new_status
        params = {"reservation_id": reservation["reservationId"], "new_startDate": new_startDate, "new_endDate": new_endDate, "new_status": new_status}
        CallAdminAPI("get", "adminRoutes/adminReservations/edit_reservation", settings.adminToken, params=params)
        print("Reservation edited succesfully. Current reservation: - StartDate:", new_startDate," - EndDate:", new_endDate," - Status:", new_status)
      else:
        print("\nNot a valid value for status. Choose either reserved, started or stopped.")
        continue
      
    elif (selection == "5"): CLIreservations()


def CLIcount(filter):
  count = 0
  reservations = getReservations(filter)
  try:
    for reservation in reservations:
      count+=1
    return count
  except TypeError:
    count
  