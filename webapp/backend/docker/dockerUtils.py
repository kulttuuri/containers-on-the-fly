from python_on_whales import docker
from database import Session, Reservation, ReservedContainerPort
from helpers.auth import create_password
from helpers.server import ORMObjectToDict
#from dateutil import parser
#from dateutil.relativedelta import *
from helpers.email import send_email
from datetime import timezone
import datetime
from helpers.auth import create_password
from settings import settings
from docker.docker_functionality import get_email_container_started, start_container, stop_container
import random
import socket
import os

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
  with Session() as session:
    allActiveReservations = session.query(Reservation).filter( Reservation.status == "started" )
    for reservation in allActiveReservations:
      for usedPort in reservation.reservedContainer.reservedContainerPorts:
        #print("Used port:", usedPort.outsidePort)
        portsInUse.append(usedPort.outsidePort)
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

import re
def removeSpecialCharacters(string):
  pattern = re.compile(r'[^a-zA-Z0-9\s]')
  return re.sub(pattern, '', string)

def timeNow():
  return datetime.datetime.now(datetime.timezone.utc)

def startDockerContainer(reservationId: str):
  with Session() as session:
    reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
    if reservation == None: return False
    sshPassword = create_password()

    imageName = reservation.reservedContainer.container.imageName
    hwSpecs = {}
    gpuSpecs = {}
    for spec in reservation.reservedHardwareSpecs:
      if spec.hardwareSpec.type == "gpu":
        gpuSpecs[spec.hardwareSpec.internalId] = { "amount": spec.amount }
      else:
        hwSpecs[spec.hardwareSpec.type] = { "amount": spec.amount }
      #print(f"{spec.hardwareSpec.type}: {spec.amount} {spec.hardwareSpec.format}")

    timeNowParsed = timeNow().strftime('%m_%d_%Y_%H_%M_%S')

    containerName = f"reservation-{reservation.reservationId}-{imageName}-{timeNowParsed}"
    reservation.reservedContainer.containerDockerName = containerName

    ports = []

    # Set bindable ports for the reservation container
    for port in reservation.reservedContainer.container.containerPorts:
      #print(port.port)
      outsidePort = get_available_port()
      ports.append({
        "containerPortId" : port.containerPortId,
        "serviceName": port.serviceName,
        "localPort": port.port,
        "outsidePort": outsidePort
      })

    userEmailParsed = removeSpecialCharacters(reservation.user.email)
    mountLocation = f'{settings.docker["mountLocation"]}/{userEmailParsed}'

    # Create the GPUs string to be passed to Docker
    gpusString = ""
    # Loop through all hwSpecs and find the reserved GPU internal IDs (Nvidia / cuda IDs), if any
    if len(gpuSpecs) > 0:
      gpusString = "device="
      for gpu in gpuSpecs:
        gpusString = gpusString + gpu + ","
      # Remove the trailing , from gpuSpecs, if it exists
      if gpusString[-1] == ",": gpusString = gpusString[:-1]

    # Create the port string to be passed to Docker
    portsForContainer = []
    for port in ports:
      portsForContainer.append( (port["outsidePort"], port["localPort"]) )

    details = {
      "name": containerName,
      "image": imageName,
      "username": "user",
      "cpus": int(hwSpecs['cpus']["amount"]),
      "gpus": gpusString,
      "memory": f"{hwSpecs['ram']['amount']}g",
      "shm_size": settings.docker["shm_size"],
      "ports": portsForContainer,
      "localMountFolderPath": mountLocation,
      "password": sshPassword
    }
    cont_was_started = False

    try:
      cont_was_started, cont_name, cont_password, non_critical_errors = start_container(details)
    except Exception as e:
      next
    
    if cont_was_started == True:
      print(f"Container with Docker name {cont_name} was started succesfully.")
      # Set bound ports
      for port in ports:
        reservation.reservedContainer.reservedContainerPorts.append(ReservedContainerPort(
          outsidePort = port["outsidePort"],
          containerPortForeign = port["containerPortId"]
        ))

      # Set basic reservation status
      reservation.status = "started"  
      reservation.reservedContainer.sshPassword = cont_password
      reservation.reservedContainer.startedAt = timeNow()
      # Send the email
      if (settings.docker["sendEmail"] == True):
        body =  get_email_container_started(
          imageName,
          reservation.computer.ip,
          ports,
          sshPassword,
          True,
          non_critical_errors,
          reservation.endDate
          )
        send_email(reservation.user.email, "AI Server is ready to use!", body)
      
      session.commit()
    else:
      # Set error message to database
      reservation.status = "error"
      reservation.reservedContainer.containerDockerErrorMessage = str(cont_name)
      session.commit()

      # Send email about the error
      if (settings.docker["sendEmail"] == True):
        body = f"Your AI server reservation did not start as there was an error. {os.linesep}{os.linesep}"
        body += f"The error was: {os.linesep}{os.linesep}{cont_name}{os.linesep}{os.linesep}"
        body += "Please do not reply to this email, this email is sent from a noreply email address."
        send_email(reservation.user.email, "AI Server did not start", body)

      print("Container was not started. Logged the error to ReservedContainer.")

def stopDockerContainer(reservationId: str):
  try:
    with Session() as session:
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
  except Exception as e:
    print("Error stopping server:")
    print(e)

def updateRunningContainerStatus(reservationId: str):
  print("IMPLEMENT")
  with Session() as session:
    reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
    print(ORMObjectToDict(reservation))
    print(ORMObjectToDict(reservation.reservedContainer))
    reservation.reservedContainer.containerStatus = "Container status here..."
    session.commit()

def getReservationsRequiringStart():
  with Session() as session:
    reservations = session.query(Reservation).filter(
      Reservation.status == "reserved",
      Reservation.startDate < timeNow()
    )
    return reservations

def getRunningReservations():
  with Session() as session:
    reservations = session.query(Reservation).filter(
      Reservation.status == "started",
      Reservation.startDate < timeNow(),
      Reservation.endDate > timeNow()
    )
    return reservations

def getReservationsRequiringStop():
  with Session() as session:
    reservations = session.query(Reservation).filter(
      Reservation.status == "started",
      Reservation.endDate < timeNow()
    )
    return reservations

def getContainerInformation(reservationId: str):
  '''
    Returns:
      On error or if cannot find the container:
        None, {}
      Otherwise (example, first is container name / ID and second is the python_on_whales.components.container.models.ContainerState object):
        "yolov7_12_12_12_2023",
        python_on_whales.components.container.models.ContainerState object {
          containerName = 'yolov7_12_12_12_2023',
          status='running',
          running=True,
          paused=False,
          restarting=False,
          oom_killed=False,
          dead=False,
          pid=1042809,
          exit_code=0,
          error='',
          started_at=datetime.datetime(2023, 5, 22, 17, 47, 42, 381981),
          tzinfo=datetime.timezone.utc),
          finished_at=datetime.datetime(1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
          health=None
        }
  '''
  try:
    with Session() as session:
      reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId ).first()
      if reservation == None:
        return None, {}
      containerState = docker.container.inspect(reservation.reservedContainer.containerDockerName)
      return reservation.reservedContainer.containerDockerName, containerState
  except Exception as e:
    print(f"Something went wrong getting container information for reservation {reservationId}. Error:")
    print(e)
    return None, {}