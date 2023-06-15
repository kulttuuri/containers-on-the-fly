from database import Session, Computer, ContainerPort, User, Reservation, Container, ReservedContainer, ReservedHardwareSpec, HardwareSpec
from dateutil import parser
from dateutil.relativedelta import *
from datetime import timezone, timedelta
from helpers.server import Response, ORMObjectToDict
import datetime
from endpoints.models.admin import ContainerEdit

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

def saveContainer(containerEdit : ContainerEdit) -> object:
  '''
  Edits the given container.

  Parameters:
    containerId: id of the container to edit.
    data: New data for the container.
  
  Returns:
    object: Response object with status, message and data.

  '''

  with Session() as session:
    # If new, create a new container
    if containerEdit.containerId == -1:
      container = Container()
      container.public = containerEdit.data.get("public", False)
      container.name = containerEdit.data.get("name")
      container.imageName = containerEdit.data.get("imageName")
      container.description = containerEdit.data.get("description", "")
      # Add ports
      for port in containerEdit.data.get("ports", []):
        container.containerPorts.append(ContainerPort(port=port["port"], serviceName=port["serviceName"]))
      session.add(container)
      session.commit()
    # Otherwise, edit container
    else:
      container = session.query(Container).filter(Container.containerId == containerEdit.containerId).first()
      if container is None:
        return Response(False, "Container not found.")
      else:
        container.public = containerEdit.data.get("public", False)
        container.name = containerEdit.data.get("name")
        container.imageName = containerEdit.data.get("imageName")
        container.description = containerEdit.data.get("description", "")
        container.updatedAt = datetime.datetime.now(datetime.timezone.utc)
        # Remove all removable ports
        for port in containerEdit.data.get("removedPorts", []):
          session.query(ContainerPort).filter(ContainerPort.containerPortId == port).delete()
        # Add all new ports
        for port in containerEdit.data.get("ports", []):
          if "containerPortId" not in port:
            container.containerPorts.append(ContainerPort(port=port["port"], serviceName=port["serviceName"]))
        # Edit changed ports
        for port in containerEdit.data.get("ports", []):
          if "containerPortId" in port:
            oldPort = session.query(ContainerPort).filter(ContainerPort.containerPortId == port["containerPortId"]).first()
            if oldPort.port != port["port"] or oldPort.serviceName != port["serviceName"]:
              oldPort.port = port["port"]
              oldPort.serviceName = port["serviceName"]
              oldPort.updatedAt = datetime.datetime.now(datetime.timezone.utc)

        #for port in containerEdit.data.get("ports", []):
        #  container.containerPorts.append(ContainerPort(port=port["port"], serviceName=port["serviceName"]))
        session.commit()
  return Response(True, "Container saved successfully")

def removeContainer(containerId : int) -> object:
  '''
  Removes the given container.

  Parameters:
    containerId: id of the container to remove.
  
  Returns:
    object: Response object with status, message and data.
  '''

  with Session() as session:
    container = session.query(Container).filter(Container.containerId == containerId).first()
    if container is None:
      return Response(False, "Container not found.")
    else:
      container.removed = True
      container.public = False
      session.commit()
  
  return Response(True, "Container removed successfully")

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
  Returns a list of all containers which have not been removed.

  Returns:
    object: Response object with status, message and data.
  '''

  data = []

  with Session() as session:
    # Find all where Container.removed is not True
    query = session.query(Container).filter(Container.removed.isnot(True))
    for container in query:
      addable = {}
      addable = ORMObjectToDict(container)
      addable["ports"] = []
      for port in container.containerPorts:
        addable["ports"].append({
          "containerPortId": port.containerPortId,
          "port": port.port,
          "serviceName": port.serviceName,
        })
      data.append(addable)
  
  return Response(True, "Data fetched.", { "containers": data })

def getContainer(containerId : int) -> object:
  '''
  Returns the given container.

  Returns:
    object: Response object with status, message and data.
  '''

  addable = {}

  with Session() as session:
    query = session.query(Container).filter(Container.containerId == containerId).limit(1)
    for container in query:
      addable = {}
      addable = ORMObjectToDict(container)
      addable["ports"] = []
      for port in container.containerPorts:
        addable["ports"].append({
          "containerPortId": port.containerPortId,
          "port": port.port,
          "serviceName": port.serviceName,
        })
  
  return Response(True, "Data fetched.", { "data": addable })

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