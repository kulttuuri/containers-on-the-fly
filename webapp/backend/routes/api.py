from fastapi import APIRouter
from endpoints import user, reservation
from settings import settings
from helpers.auth import HashPassword
from database import session, User, Role, Computer, HardwareSpec, UserStorage, Container

router = APIRouter()
router.include_router(user.router)
router.include_router(reservation.router)

# Run code here when server starts

if settings.app["production"] == True:
  print("Running server in production mode")

# Add test data if running in development mode
if settings.app["production"] == False:
  print("Running server in development mode")

  # Admin role
  adminRole = session.query(Role).filter( Role.name == "admin" ).first()
  if adminRole is None:
    print("Creating test data: admin role with name admin")
    session.add(Role(
      name = "admin"
    ))
    session.commit()
  
  # Admin user
  adminUser = session.query(User).filter( User.email == "aiserveradmin@samk.fi" ).first()
  if adminUser is None:
    print("Creating test data: admin user with email aiserveradmin@samk.fi")
    hash = HashPassword("test")
    adminUser = User(
      email = "aiserveradmin@samk.fi",
      password = hash["hashedPassword"],
      passwordSalt = hash["salt"]
    )
    adminRole = session.query(Role).filter( Role.name == "admin" ).first()
    adminUser.roles.append(adminRole)
    adminUser.userStorage.append(UserStorage( maxSpace = "10000", maxSpaceFormat = "mb" ))
    session.add(adminUser)
    session.commit()
  
  # Normal User
  normalUser = session.query(User).filter( User.email == "aiserveruser@samk.fi" ).first()
  if normalUser is None:
    print("Creating test data: normal user with email aiserveruser@samk.fi")
    hash = HashPassword("test")
    normalUser = User(
      email = "aiserveruser@samk.fi",
      password = hash["hashedPassword"],
      passwordSalt = hash["salt"]
    )
    normalUser.userStorage.append(UserStorage( maxSpace = "5000", maxSpaceFormat = "mb" ))
    session.add(normalUser)
    session.commit()

  # Computer
  computer = session.query(Computer).filter( Computer.name == "aiserver" ).first()
  if computer is None:
    print("Creating test data: computer named aiserver")
    computer = Computer( name = "aiserver" )
    session.add(computer)
    session.commit()

  # Hardware Specs for computer
  computer = session.query(Computer).filter( Computer.name == "aiserver" ).first()
  if len(computer.hardwareSpecs) == 0:
    print("Creating test data: hardware specs for a computer")
    computer.hardwareSpecs.append(HardwareSpec(
      type = "GPU",
      maximumAmount = 6,
      maximumAmountForUser = 2,
      defaultAmountForUser = 1,
      minimumAmount = 0,
      format = "GPUs",
    ))
    computer.hardwareSpecs.append(HardwareSpec(
      type = "RAM",
      maximumAmount = 500,
      maximumAmountForUser = 50,
      defaultAmountForUser = 10,
      minimumAmount = 2,
      format = "GB",
    ))
    computer.hardwareSpecs.append(HardwareSpec(
      type = "CPU threads",
      maximumAmount = 80,
      maximumAmountForUser = 10,
      defaultAmountForUser = 5,
      minimumAmount = 1,
      format = "Threads",
    ))
    session.commit()

  # Container
  container = session.query(Container).filter( Container.imageName == "ubuntu2004" ).first()
  if container is None:
    print("Creating test data: container with name Ubuntu 20.04")
    container = Container(
      imageName = "ubuntu2004",
      name = "Ubuntu 20.04",
      description = "Empty Ubuntu 20.04 container"
    )
    session.add(container)
    session.commit()