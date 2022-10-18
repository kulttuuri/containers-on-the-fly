from database import Session, Reservation, ReservedContainerPort
from helpers.auth import create_password
from helpers.server import ORMObjectToDict
#from dateutil import parser
#from dateutil.relativedelta import *
from datetime import timezone
import datetime
from helpers.auth import create_password
from settings import settings
from docker.docker_functionality import send_email_container_started, start_container, stop_container
import random
import socket

def is_port_in_use(port: int) -> bool:
  '''
  Checks if a port is in use.
  Returns:
    True if port is in use, False otherwise
  '''
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    return s.connect_ex(('localhost', port)) == 0

def get_available_port():
  # Loop through all started containers and get the ports in use
  portsInUse = []
  session = Session()
  allActiveReservations = session.query(Reservation).filter( Reservation.status == "started" )
  for reservation in allActiveReservations:
    for usedPort in reservation.reservedContainer.reservedContainerPorts:
      #print("Used port:", usedPort.outsidePort)
      portsInUse.append(usedPort.outsidePort)
  session.close()
  min = settings.docker["port_range_start"]
  max = settings.docker["port_range_end"]
  availablePorts = []
  for port in range(min, max):
    if port not in portsInUse:
      availablePorts.append(port)
  
  # Try to bind to a random available port 5 times
  i = 0
  retries = 5
  while i < retries:
    randPort = random.choice(availablePorts)
    if is_port_in_use(randPort) == False:
       return randPort
    i += 1

  return random.choice(availablePorts)

def timeNow():
  return datetime.datetime.now(datetime.timezone.utc)

def startDockerContainer(reservationId: str):
  session = Session()
  reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
  if reservation == None: return False
  sshPassword = create_password()

  imageName = reservation.reservedContainer.container.imageName
  hwSpecs = {}
  for spec in reservation.reservedHardwareSpecs:
    hwSpecs[spec.hardwareSpec.type] = spec.amount
    #print(f"{spec.hardwareSpec.type}: {spec.amount} {spec.hardwareSpec.format}")

  timeNowParsed = timeNow().strftime('%m_%d_%Y_%H_%M_%S')

  containerName = f"reservation-{reservation.reservationId}-{imageName}-{timeNowParsed}"
  reservation.reservedContainer.containerDockerName = containerName

  bindablePorts = []
  portsForEmail = []

  # Set bindable ports for the reservation container
  for port in reservation.reservedContainer.container.containerPorts:
    #print(port.port)
    outsidePort = get_available_port()
    bindablePorts.append( (outsidePort, port.port) )
    portsForEmail.append({ "serviceName": port.serviceName, "localPort": port.port, "outsidePort": outsidePort })

  details = {
    "name": containerName,
    "image": imageName,
    "username": "user",
    "cpus": int(hwSpecs['cpus']),
    "gpus": int(hwSpecs['gpus']),
    "memory": f"{hwSpecs['ram']}g",
    "shm_size": settings.docker["shm_size"],
    "ports": bindablePorts,
    "localMountFolderPath": settings.docker["mountLocation"],
    "password": sshPassword
  }
  cont_was_started = False

  try:
    cont_was_started, cont_name, cont_password = start_container(details)
  except Exception as e:
    #print("Error starting container:", e)
    session.close()
  
  if cont_was_started == True:
    print("Container was started succesfully.")
    # Set bound ports
    for port in bindablePorts:
      reservation.reservedContainer.reservedContainerPorts.append(ReservedContainerPort(
        outsidePort = port[0],
        localPort = port[1]
      ))

    # Set basic reservation status
    reservation.status = "started"  
    reservation.reservedContainer.sshPassword = cont_password
    reservation.reservedContainer.startedAt = timeNow()
    # Send the email
    if (settings.docker["sendEmail"] == True):
      send_email_container_started(
        reservation.user.email,
        imageName,
        reservation.computer.ip,
        portsForEmail,
        sshPassword,
        reservation.endDate)
    
    session.commit()
    session.close()
  else:
    print("Container was not started.")

def stopDockerContainer(reservationId: str):
  session = Session()
  reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
  if reservation == None: return False

  # Can use reservation.reservedContainer.containerDockerId to target the docker container
  #print("STOPPING CONTAINER:")
  #print(ORMObjectToDict(reservation))
  #print(ORMObjectToDict(reservation.reservedContainer))
  stop_container(reservation.reservedContainer.containerDockerName)
  reservation.status = "stopped"
  reservation.reservedContainer.stoppedAt = timeNow()
  session.commit()
  session.close()

def updateRunningContainerStatus(reservationId: str):
  print("IMPLEMENT")
  session = Session()
  reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
  print(ORMObjectToDict(reservation))
  print(ORMObjectToDict(reservation.reservedContainer))
  reservation.reservedContainer.containerStatus = "Container status here..."
  session.commit()
  session.close()

def getReservationsRequiringStart():
  session = Session()
  reservations = session.query(Reservation).filter(
    Reservation.status == "reserved",
    Reservation.startDate < timeNow()
  )
  session.close()
  return reservations

def getRunningReservations():
  session = Session()
  reservations = session.query(Reservation).filter(
    Reservation.status == "started",
    Reservation.startDate < timeNow(),
    Reservation.endDate > timeNow()
  )
  session.close()
  return reservations

def getReservationsRequiringStop():
  session = Session()
  reservations = session.query(Reservation).filter(
    Reservation.status == "started",
    Reservation.endDate < timeNow()
  )
  session.close()
  return reservations