from docker.dockerUtils import getContainerInformation, getRunningReservations, getReservationsRequiringStart, getReservationsRequiringStop, stopDockerContainer, startDockerContainer
from docker.docker_functionality import restart_container

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
    restartCrashedServers()
    sleep(15)

def startNewServers():
  reservations = getReservationsRequiringStart()
  for reservation in reservations:
    if settings.docker["enabled"] == True:
      print(timeNow(), ": Starting Docker server for reservation with reservationId: ",  reservation.reservationId)
      startDockerContainer(reservation.reservationId)

def restartCrashedServers():
  reservations = getRunningReservations()
  for reservation in reservations:
    if settings.docker["enabled"] == True:
      try:
        containerName, containerState = getContainerInformation(reservation.reservationId)
        #print(containerName, containerState)
        #print(containerState.state.status)
        if containerState.state.status == "exited":
          restart_container(containerName)
      except Exception as e:
        print(f"Error restarting a container:")
        print(e)
        pass
      
      #print(timeNow(), ": Restarting Docker server for reservation with reservationId: ",  reservation.reservationId)
      #startDockerContainer(reservation.reservationId)

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