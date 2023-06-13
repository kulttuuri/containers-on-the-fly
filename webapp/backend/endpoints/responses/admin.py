from database import Session, Computer, User, Reservation, Container, ReservedContainer, ReservedHardwareSpec, HardwareSpec
from dateutil import parser
from dateutil.relativedelta import *
from datetime import timezone, timedelta
from helpers.server import Response, ORMObjectToDict
import datetime

def getReservations() -> object:
  '''
  Returns a list of all reservations.

  Returns:
    object: Response object with status, message and data.
  '''
  reservations = []

  # Limit listing to 90 days
  def timeNow(): return datetime.datetime.now(datetime.timezone.utc)
  minStartDate = timeNow() - timedelta(days=90)

  with Session() as session:
    query = session.query(Reservation).filter(Reservation.startDate > minStartDate )
  for reservation in query:
    res = ORMObjectToDict(reservation)
    res["userEmail"] = reservation.user.email
    res["reservedContainer"] = ORMObjectToDict(reservation.reservedContainer)
    res["reservedContainer"]["container"] = ORMObjectToDict(reservation.reservedContainer.container)
    # Add all reserved hardware specs
    res["reservedHardwareSpecs"] = []
    for spec in reservation.reservedHardwareSpecs:
      # Add only specs over 0
      if spec.amount > 0:
          # Add also internalId for GPUs
          if spec.hardwareSpec.type == "gpu":
            format = f"{spec.hardwareSpec.format} (id: {spec.hardwareSpec.internalId})"
          else:
            format = spec.hardwareSpec.format

          res["reservedHardwareSpecs"].append({
            "type": spec.hardwareSpec.type,
            "format": format,
            "internalId": spec.hardwareSpec.format,
            "amount": spec.amount
          })
    reservations.append(res)
    
  return Response(True, "Reservations fetched.", { "reservations": reservations })

def getUsers() -> object:
  '''
  Returns a list of all users.

  Returns:
    object: Response object with status, message and data.
  '''

  data = []

  with Session() as session:
    query = session.query(User)
    for user in query:
      addable = {}
      addable["userId"] = user.userId
      addable["email"] = user.email
      addable["createdAt"] = user.userCreatedAt
      data.append(addable)
  
  return Response(True, "Users fetched.", { "users": data })

def getHardware() -> object:
  '''
  Returns a list of all hardware.

  Returns:
    object: Response object with status, message and data.
  '''

  data = []

  with Session() as session:
    query = session.query(HardwareSpec)
    for hardware in query:
      addable = {}
      addable = ORMObjectToDict(hardware)
      data.append(addable)
  
  return Response(True, "Data fetched.", { "hardware": data })

def getContainers() -> object:
  '''
  Returns a list of all containers.

  Returns:
    object: Response object with status, message and data.
  '''

  data = []

  with Session() as session:
    query = session.query(Container)
    for container in query:
      addable = {}
      addable = ORMObjectToDict(container)
      data.append(addable)
  
  return Response(True, "Data fetched.", { "containers": data })

def editReservation(reservationId : int, endDate : str) -> object:
  '''
  Edits the given reservation.

  Parameters:
    reservationId: id of the reservation to edit.
    endDate: New end date for the reservation.

  Returns:
    object: Response object with status, message and data.
  '''
  # Verify that the new end date is valid
  try:
    endDate = parser.parse(endDate)
  except:
    return Response(False, "Invalid end date.")

  with Session() as session:
    reservation = session.query(Reservation).filter(Reservation.reservationId == reservationId).first()
    if reservation is None:
      return Response(False, "Reservation not found.")
    else:
      reservation.endDate = endDate
      session.commit()

  return Response(True, "Reservation was edited succesfully.")