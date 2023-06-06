from database import Session, Computer, User, Reservation, Container, ReservedContainer, ReservedHardwareSpec, HardwareSpec
from docker.docker_functionality import get_email_container_started
from helpers.server import Response, ORMObjectToDict
from helpers.auth import IsAdmin
from dateutil import parser
from dateutil.relativedelta import *
import datetime
from datetime import timezone, timedelta
from docker.dockerUtils import stop_container
from settings import settings

# TODO: Should be able to send a computer here and get the available hardware specs for it.
# TODO: Should also be able to only fail there is not enough resources any computer. Right now it fails if any of the computers are out of resources for the given time period.
def getAvailableHardware(date : str, duration : int, reducableSpecs : dict = None) -> object:
  '''
  Returns a list of all available hardware specs for the given date and duration.
  
  Args:
    date (str): The date when the reservation starts.
    duration (int): The duration of the reservation in hours.
    reducableSpecs (dict): If reducableSpecs is given, it will reduce the available hardware specs by the given amount.
      Example: { "1": 1, "2": 0, ... }
      Where the key is the hardwareSpecId and the value is the amount to reduce.
    
  Returns:
    object: Response object with status, message and data.

    If status is True, data will contain a list of all available hardware specs for the given date and duration.
    If status is False, message will contain the error message. The error is usually that there are not enough resources for the given date and duration.
  '''
  date = parser.parse(date)
  endDate = date+relativedelta(hours=+duration)

  with Session() as session:
  
    reservations = session.query(Reservation).filter(
      Reservation.startDate < endDate,
      Reservation.endDate > date,
      (Reservation.status == "reserved") | (Reservation.status == "started")
    )

    # All reserved hardware specs for the given time period will be listed here
    # This loop will go through all reservations and add the reserved hardware specs to this list for the given time period
    removableHardwareSpecs = {}
    for res in reservations:
      for spec in res.reservedHardwareSpecs:
        hardwareSpecId = spec.hardwareSpec.hardwareSpecId
        amount = spec.amount
        
        if hardwareSpecId not in removableHardwareSpecs:
          removableHardwareSpecs[hardwareSpecId] = amount
        else:
          removableHardwareSpecs[hardwareSpecId] += amount

    # Reduce the available hardware specs by the given reducable specs, if any
    if reducableSpecs != None:
      for key, val in reducableSpecs.items():
        intKey = int(key)
        if val == 0: continue
        if intKey not in removableHardwareSpecs:
          removableHardwareSpecs[intKey] = val
        else:
          removableHardwareSpecs[intKey] += val

    #print("removableHardwareSpecs: ", removableHardwareSpecs)

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

    for computer in computers:
      for spec in computer["hardwareSpecs"]:
        if spec["hardwareSpecId"] in removableHardwareSpecs:
          spec["maximumAmount"] -= removableHardwareSpecs[spec["hardwareSpecId"]]
          if spec["maximumAmountForUser"] > spec["maximumAmount"]:
            spec["maximumAmountForUser"] = spec["maximumAmount"]
          #print("Reducing spec: ", spec["type"], " ", removableHardwareSpecs[spec["type"]], " max: " , spec["maximumAmount"], "maxForUser: ", spec["maximumAmountForUser"])
          if spec["maximumAmount"] < spec["minimumAmount"]:
            print("Spec: ", spec["type"], " ", spec["maximumAmount"], " is below minimum amount: ", spec["minimumAmount"])
            #print("minimumAmount: ", spec["minimumAmount"])
            #print("maximumAmount: ", spec["maximumAmount"])
            #print("maximumAmountForUser: ", spec["maximumAmountForUser"])
            specMessage = ""
            specMax = spec['maximumAmount']
            if specMax < 0: specMax = 0
            if spec["type"] == "ram":
              specMessage = f"Available: {specMax} {spec['format']} {spec['type']}."
            else:
              specMessage = f"Available: {specMax} {spec['type']}."
            return Response(False, f"Not enough resources to make a reservation: {spec['type']}. {specMessage}")

    return Response(True, "Hardware resources fetched.", { "computers": computers, "containers": containers })

def getOwnReservations(userId) -> object:
  reservations = []

  # Limit listing to 90 days
  def timeNow(): return datetime.datetime.now(datetime.timezone.utc)
  minStartDate = timeNow() - timedelta(days=90)

  with Session() as session:
    query = session.query(Reservation).filter( Reservation.userId == userId, Reservation.startDate > minStartDate )
  for reservation in query:
    res = ORMObjectToDict(reservation)
    res["reservedContainer"] = ORMObjectToDict(reservation.reservedContainer)
    res["reservedContainer"]["container"] = ORMObjectToDict(reservation.reservedContainer.container)
    # Add all reserved hardware specs
    # Add only specs over 0
    res["reservedHardwareSpecs"] = []
    for spec in reservation.reservedHardwareSpecs:
      if spec.amount > 0:
        res["reservedHardwareSpecs"].append({
          "type": spec.hardwareSpec.type,
          "format": spec.hardwareSpec.format,
          "amount": spec.amount
        })
    reservations.append(res)
  
  return Response(True, "Hardware resources fetched.", { "reservations": reservations })

def getOwnReservationDetails(reservationId, userId) -> object:
  with Session() as session:
    # Check that the reservation exists and is owned by the current user
    reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId, Reservation.userId == userId ).first()
    if (reservation == None):
      return Response(False, "Reservation not found.")

    portsForEmail = []

    # Set bindable ports for the reservation container
    for port in reservation.reservedContainer.reservedContainerPorts:
      serviceName = port.containerPort.serviceName
      outsidePort = port.outsidePort
      localPort = port.localPort
      portsForEmail.append({ "serviceName": serviceName, "localPort": localPort, "outsidePort": outsidePort })

    connectionText = get_email_container_started(
      reservation.reservedContainer.container.imageName,
      reservation.computer.ip,
      portsForEmail,
      reservation.reservedContainer.sshPassword,
      False,
      reservation.endDate
      )

    connectionText = connectionText.replace("\n", "<br>")

  return Response(True, "Details fetched.", { "connectionText": connectionText } )

def getCurrentReservations() -> object:
  reservations = []

  def timeNow(): return datetime.datetime.now(datetime.timezone.utc)
  minStartDate = timeNow() - timedelta(days=14)

  with Session() as session:
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
      "computerId": reservation.computerId,
      "computerName": reservation.computer.name,
      "hardwareSpecs": specs,
    }
    reservations.append(res)
  
  return Response(True, "Current reservations fetched.", { "reservations": reservations })

def createReservation(userId, date: str, duration: int, computerId: int, containerId: int, hardwareSpecs):
  # Make sure that there are enough resources for the reservation
  getAvailableHardwareResponse = getAvailableHardware(date, duration, hardwareSpecs)
  if (getAvailableHardwareResponse["status"] == False):
    return Response(False, getAvailableHardwareResponse["message"])

  date = parser.parse(date)
  endDate = date+relativedelta(hours=+duration)

  with Session() as session:

    # Check that user exists
    user = session.query(User).filter( User.userId == userId ).first()
    if (user == None):
      return Response(False, "User not found.")
    isAdmin = IsAdmin(user.email)

    # Check that computer and container exists
    computer = session.query(Computer).filter( Computer.computerId == computerId ).first()
    if (computer == None):
      return Response(False, "Computer not found.")
    container = session.query(Container).filter( Container.containerId == containerId ).first()
    if (container == None):
      return Response(False, "Container not found.")

    # Make sure that user can only have one queued / started server at once (admins can have unlimited)
    userActiveReservations = session.query(Reservation).filter(
      (Reservation.userId == userId),
      ( (Reservation.status == "reserved") | (Reservation.status == "started") )
    ).count()
    if userActiveReservations > 0 and isAdmin == False:
      return Response(False, "You can only have one queued or started reservation.")

    # Check that the duration is between minimum and maximum lengths
    if (duration < settings.reservation["minimumDuration"]):
      return Response(False, f"Minimum duration is {settings.reservation['minimumDuration']} hours.")
    if (duration > settings.reservation["maximumDuration"]):
      return Response(False, f"Maximum duration is {settings.reservation['maximumDuration']} hours.")

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
      # Only add resources over 0
      if val > 0:
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

    informByEmail = settings.docker["sendEmail"]

    return Response(True, "Reservation created succesfully!", { "informByEmail": informByEmail })

def cancelReservation(userId, reservationId: str):
  # Check that user owns the given reservation and it can be found
  
  with Session() as session:
    reservation = session.query(Reservation).filter( Reservation.reservationId == reservationId, Reservation.userId == userId ).first()
    if reservation is None: return Response(False, "No reservation found.")

    if (reservation.status == "started"):
      stop_container(reservation.reservedContainer.containerDockerName)

    reservation.status = "stopped"
    reservation.endDate = datetime.datetime.now(datetime.timezone.utc)

    session.commit()

  return Response(True, "Reservation cancelled.")