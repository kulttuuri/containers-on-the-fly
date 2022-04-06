from database import session, Computer, User, Reservation
from helpers.server import Response, ORMObjectToDict

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
  
  return Response(True, "Hardware resources fetched.", { "computers": computers })

def createReservation(userId, date: str, duration: int, computerId: int, hardwareSpecs):
  print(date, duration, computerId, hardwareSpecs)
  print("IMPLEMENT RESERVATION CREATE NOW!")
  # TODO: CALCULATE END DATE
  #endDate = 

  # TODO: Implement reservation now
  user = session.query(User).filter( User.userId == userId ).first()
  reservation = Reservation(
    reservedContainerId = 1,
    startDate = date,
    #endDate = date
  )
  #user.reservations.append(reservation)
  #session.commit()

  return Response(False, "Not yet implemented.")