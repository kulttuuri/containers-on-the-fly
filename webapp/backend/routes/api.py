from fastapi import APIRouter
from endpoints import user
from settings import settings
from helpers.auth import hashPassword, isCorrectPassword
from database import session, User, Role, Computer, HardwareSpec, UserStorage

router = APIRouter()
router.include_router(user.router)

# Run code here when server starts

# Add test data if running in development mode
if settings.app["production"] == False:
  print("Running server in development mode")

  # Admin role
  adminRole = session.query(Role).filter( Role.name == "admin" ).first()
  if adminRole is None:
    print("Creating test data: admin role")
    session.add(Role(
      name = "admin"
    ))
    session.commit()
  
  # Admin user
  adminUser = session.query(User).filter( User.email == "aiserveradmin@samk.fi" ).first()
  if adminUser is None:
    print("Creating test data: admin user")
    hash = hashPassword("test")
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
    print("Creating test data: normal user")
    hash = hashPassword("test")
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
    computer = Computer( name = "aiserver" )
    session.add(computer)
    session.commit()

  # Hardware Specs for computer

  # Container
  