from database import session, Computer
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