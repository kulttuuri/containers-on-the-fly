from database import session, Computer, User, Reservation, Container, ReservedContainer, ReservedHardwareSpec, HardwareSpec
from helpers.server import Response, ORMObjectToDict
from helpers.auth import IsAdmin
from dateutil import parser
from dateutil.relativedelta import *
import datetime
from datetime import timezone, timedelta

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

def getOwnReservations(userId) -> object:
  session.commit()
  reservations = []

  # Limit listing to 90 days
  def timeNow(): return datetime.datetime.now(datetime.timezone.utc)
  minStartDate = timeNow() - timedelta(days=90)

  query = session.query(Reservation).filter( Reservation.userId == userId, Reservation.startDate > minStartDate )
  for reservation in query:
    res = ORMObjectToDict(reservation)
    res["reservedContainer"] = ORMObjectToDict(reservation.reservedContainer)
    res["reservedContainer"]["container"] = ORMObjectToDict(reservation.reservedContainer.container)
    reservations.append(reservation)
  
  return Response(True, "Hardware resources fetched.", { "reservations": reservations })

def getCurrentReservations() -> object:
  session.commit()
  reservations = []

  def timeNow(): return datetime.datetime.now(datetime.timezone.utc)
  minStartDate = timeNow() - timedelta(days=14)

  query = session.query(Reservation).filter(
    ((Reservation.status == "reserved") | (Reservation.status == "started")),
    (Reservation.startDate > minStartDate)
  )
  for reservation in query:
    specs = []
    for spec in reservation.reservedHardwareSpecs:
      specs.append({
        "type": spec.hardwareSpec.type,
        "format": spec.hardwareSpec.format,
        "amount": spec.amount,
      })
    res = {
      "reservationId": reservation.reservationId,
      "startDate": reservation.startDate,
      "endDate": reservation.endDate,
      "hardwareSpecs": specs,
    }
    reservations.append(res)
  
  return Response(True, "Current reservations fetched.", { "reservations": reservations })

def createReservation(userId, date: str, duration: int, computerId: int, containerId: int, hardwareSpecs):
  session.commit()

  date = parser.parse(date)
  endDate = date+relativedelta(hours=+duration)
  user = session.query(User).filter( User.userId == userId ).first()
  if (user == None): return Response(False, "User not found.")
  isAdmin = IsAdmin(user.email)

  # TODO: Make sure that there are enough resources for the reservation

  # Make sure that user can only have one queued / started server at once (admins can have unlimited)
  userActiveReservations = session.query(Reservation).filter(
    (Reservation.userId == userId),
    ( (Reservation.status == "reserved") | (Reservation.status == "started") )
  ).count()
  if userActiveReservations > 0 and isAdmin == False:
    return Response(False, "You can only have one queued or started reservation.")

  # Create the base reservation
  reservation = Reservation(
    reservedContainerId = containerId,
    startDate = date,
    endDate = endDate,
    userId = user.userId,
    computerId = computerId,
    status = "reserved",
  )
  session.add(reservation)
  #print(reservation)
  #reservation = session.query(Reservation).filter(  )
  # Append all reserved hardware specs inside the reservation
  for key, val in hardwareSpecs.items():
    # Check that the amount does not exceed user limits for the given hardware
    hardwareSpec = session.query(HardwareSpec).filter( HardwareSpec.hardwareSpecId == key ).first()
    if val > hardwareSpec.maximumAmountForUser: raise Exception("Trying to utilize hardware specs above the user maximum amount")
    session.add(
      ReservedHardwareSpec(
        reservationId = reservation.reservationId,
        hardwareSpecId = key,
        amount = val,
      )
    )
  # Create the ReservedContainer
  reservation.reservedContainer = ReservedContainer(
    containerId = containerId,
  )
  #print(ORMObjectToDict(reservation))
  #print(ORMObjectToDict(reservation.reservedContainer))
  user.reservations.append(reservation)
  session.commit()

  return Response(True, "Reservation created succesfully!")

def cancelReservation(userId, reservationId: str):
  # Check that user owns the given reservation and it can be found
  reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId, Reservation.userId == userId ).first()
  if reservation is None: return Response(False, "No reservation found.")

  # TODO: Use also the Docker method here that will do this
  reservation.status = "stopped"
  session.commit()

  return Response(True, "Reservation cancelled.")