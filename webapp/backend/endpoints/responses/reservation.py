from database import session, Computer, User, Reservation, Container, ReservedContainer, ReservedHardwareSpec, HardwareSpec
from helpers.server import Response, ORMObjectToDict
from dateutil import parser
from dateutil.relativedelta import *

def getAvailableHardware(date) -> object:
  # TODO: Get only available resources for this time period

  computers = []

  allComputers = session.query(Computer)
  for computer in allComputers:
    compDict = ORMObjectToDict(computer)
    compDict["hardwareSpecs"] = []
    for spec in computer.hardwareSpecs:
      compDict["hardwareSpecs"].append(ORMObjectToDict(spec))
    computers.append(compDict)

  containers = []
  allContainers = session.query(Container)
  for container in allContainers:
    containers.append(ORMObjectToDict(container))
  
  return Response(True, "Hardware resources fetched.", { "computers": computers, "containers": containers })

def createReservation(userId, date: str, duration: int, computerId: int, containerId: int, hardwareSpecs):
  # TODO: Make sure that user can only have one queued / started server at once
  # TODO: Make sure that there are enough resources for the reservation
  
  #print(date, duration, computerId, hardwareSpecs)
  print("IMPLEMENT RESERVATION CREATE NOW!")

  date = parser.parse(date)
  endDate = date+relativedelta(hours=+duration)
  user = session.query(User).filter( User.userId == userId ).first()

  # Create the base reservation
  reservation = Reservation(
    reservedContainerId = containerId,
    startDate = date,
    endDate = endDate,
    userId = user.userId,
    computerId = computerId,
  )
  session.add(reservation)
  print(reservation)
  #reservation = session.query(Reservation).filter(  )
  # Append all reserved hardware specs inside the reservation
  for key, val in hardwareSpecs.items():
    # TODO: Check that the amount does not exceed user limits for the given hardware
    hardwareSpec = session.query(HardwareSpec).filter( HardwareSpec.hardwareSpecId == key ).first()
    if val > hardwareSpec.maximumAmountForUser: raise Exception("Trying to utilize hardware specs above the user maximum amount")
    session.add(
      ReservedHardwareSpec(
        reservationId = reservation.reservationId,
        hardwareSpecId = key,
        amount = val
      )
    )
  # Create the ReservedContainer
  reservation.reservedContainer = ReservedContainer(
    containerId = containerId,
    status = "reserved"
  )
  print("!!!OK!!!")
  print(ORMObjectToDict(reservation))
  print(ORMObjectToDict(reservation.reservedContainer))
  # TODO: Try adding to DB now...
  #user.reservations.append(reservation)
  session.commit()

  return Response(False, "Not yet implemented.")