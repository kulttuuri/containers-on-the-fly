from docker.dockerUtils import getReservationsRequiringStart, startDockerContainer

from time import sleep
run = True

import datetime
from datetime import timezone

def timeNow():
  return datetime.datetime.now(datetime.timezone.utc)

def main():
  while (run):
    startNewServers()
    stopFinishedServers()
    sleep(15)

def startNewServers():
  reservations = getReservationsRequiringStart()
  for reservation in reservations:
    print(timeNow(), ": Starting Docker server for reservation with reservationId: ",  reservation.reservationId)
    print(reservation.startDate)
    startDockerContainer(reservation.reservationId)

def stopFinishedServers():
  #print("Stopping finished servers...")
  return None

if __name__ == "__main__":
  main()