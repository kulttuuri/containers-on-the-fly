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
    if (settings.docker['enabled'] != True):
      print("!!! Docker support has not been enabled, so this script does nothing. Enable it with settings.json setting docker.enabled: true !!!")
    stopFinishedServers()
    startNewServers()
    sleep(15)

def startNewServers():
  reservations = getReservationsRequiringStart()
  for reservation in reservations:
    if settings.docker["enabled"] == True:
      print(timeNow(), ": Starting Docker server for reservation with reservationId: ",  reservation.reservationId)
      startDockerContainer(reservation.reservationId)

def stopFinishedServers():
  reservations = getReservationsRequiringStop()
  for reservation in reservations:
    if settings.docker["enabled"] == True:
      print(timeNow(), ": Stopping Docker server for reservation with reservationId: ",  reservation.reservationId)
      stopDockerContainer(reservation.reservationId)

if __name__ == "__main__":
  print("AI Server Docker utility started.")
  print("This software will run infinitely and start / stop servers for reservations.")
  main()