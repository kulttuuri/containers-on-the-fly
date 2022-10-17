from docker.dockerUtils import getReservationsRequiringStart, getReservationsRequiringStop, stopDockerContainer, startDockerContainer

from time import sleep
run = True

from settings import settings

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
    if settings.docker["enabled"] == True:
      startDockerContainer(reservation.reservationId)

def stopFinishedServers():
  reservations = getReservationsRequiringStop()
  for reservation in reservations:
    print(timeNow(), ": Stopping Docker server for reservation with reservationId: ",  reservation.reservationId)
    if settings.docker["enabled"] == True:
      stopDockerContainer(reservation.reservationId)

if __name__ == "__main__":
  print("AI Server Docker utility started.")
  print("This software will run infinitely and start / stop servers for reservations.")
  main()