from database import session, Reservation
from helpers.server import ORMObjectToDict
#from dateutil import parser
#from dateutil.relativedelta import *
import datetime
from datetime import timezone
import random
import string

def generateSSHPassword():
  characters = string.ascii_letters + string.digits + string.punctuation
  password = ''.join(random.choice(characters) for i in range(50))
  return password

def timeNow():
  return datetime.datetime.now(datetime.timezone.utc)

def startDockerContainer(reservationId: str):
  session.commit()
  reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
  if reservation == None: return False
  now = timeNow()
  sshPassword = generateSSHPassword()
  
  # TODO: Start the actual Docker container here
  # TODO: Email connection details for the user
  print(sshPassword) # Password generated here
  reservation.reservedContainer.containerDockerId = "..." # Add the container ID marked in Docker here
  print("RESERVATION:")
  print(ORMObjectToDict(reservation))
  print("USER:")
  print(ORMObjectToDict(reservation.user))
  print("RESERVED CONTAINER:")
  print(ORMObjectToDict(reservation.reservedContainer))
  print("CONTAINER:")
  print(ORMObjectToDict(reservation.reservedContainer.container))
  print("HARDWARE SPECS:")
  for spec in reservation.reservedHardwareSpecs:
    print(f"{spec.hardwareSpec.type}: {spec.amount} {spec.hardwareSpec.format}")
  #print(ORMObjectToDict(reservation.reservedHardwareSpecs))

  reservation.status = "started"
  reservation.reservedContainer.sshPassword = sshPassword
  reservation.reservedContainer.startedAt = now
  session.commit()

def stopDockerContainer(reservationId: str):
  session.commit()
  reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
  if reservation == None: return False
  now = timeNow()

  # TODO: Stop the actual container here
  # Can use reservation.reservedContainer.containerDockerId to target the docker container
  print(ORMObjectToDict(reservation))
  print(ORMObjectToDict(reservation.reservedContainer))

  reservation.status = "stopped"
  reservation.reservedContainer.stoppedAt = now
  session.commit()

def updateRunningContainerStatus(reservationId: str):
  print("IMPLEMENT")
  session.commit()
  reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
  reservation.reservedContainer.containerStatus = "Container status here..."
  session.commit()

def getReservationsRequiringStart():
  reservations = session.query(Reservation).filter(
    Reservation.status == "reserved",
    Reservation.startDate < timeNow()
  )
  return reservations

def getRunningReservations():
  reservations = session.query(Reservation).filter(
    Reservation.status == "started",
    Reservation.startDate < timeNow(),
    Reservation.endDate > timeNow()
  )
  return reservations

def getReservationsRequiringStop():
  reservations = session.query(Reservation).filter(
    Reservation.status == "started",
    Reservation.endDate < timeNow()
  )
  return reservations