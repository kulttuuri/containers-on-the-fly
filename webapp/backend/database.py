from sqlalchemy import create_engine
from settings import settings
engine = create_engine(settings.database["engineUri"] + settings.database["filePath"], echo=settings.database["debugPrinting"], future=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "User"
  userId = Column(Integer, primary_key = True, autoincrement = True)
  email = Column(String, nullable = False)
  studentId = Column(String, nullable = True)
  loginToken = Column(String, nullable = True)
  loginTokenCreatedAt = Column(DateTime, nullable = True)
  userCreatedAt = Column(DateTime, nullable = False)

  loginTypeAd = relationship("LoginTypeAD", back_populates = "User")
  loginTypePassword = relationship("LoginTypePassword", back_populates = "User")
  userStorage = relationship("UserStorage", back_populates = "User")
  roles = relationship("Role", secondary = "UserRole", back_populates = "User", single_parent=True)
  reservations = relationship("Reservation", back_populates = "User")

class LoginTypeAD(Base):
  __tablename__ = "LoginTypeAD"
  loginTypeADId = Column(Integer, primary_key = True, autoincrement = True)
  userId = Column(ForeignKey('User.userId'), unique = True, nullable = False)
  user = relationship("User", back_populates = "LoginTypeAD")

class LoginTypePassword(Base):
  __tablename__ = "LoginTypePassword"
  loginTypePasswordId = Column(Integer, primary_key = True, autoincrement = True)
  userId = Column(ForeignKey('User.userId'), unique = True, nullable = False)
  password = Column(String, nullable = False)
  user = relationship("User", back_populates = "LoginTypeAD")

class UserStorage(Base):
  __tablename__ = "UserStorage"
  userStorageId = Column(Integer, primary_key = True, autoincrement = True)
  userId = Column(ForeignKey('User.userId'), unique = True, nullable = False)
  maxSpace = Column(Float, nullable = False)
  maxSpaceFormat = Column(String, nullable = False)
  UniqueConstraint('userStorageId', 'userId', name='uniqueUserStorage')
  user = relationship("User", back_populates = "LoginTypeAD")

class Role(Base):
  __tablename__ = "Role"
  roleId = Column(Integer, primary_key = True, autoincrement = True)
  name = Column(String, nullable = False, unique = True)
  createdAt = Column(DateTime, nullable = False)
  users = relationship("User", secondary = "UserRole", back_populates = "Role", single_parent=True)

class UserRole(Base):
  __tablename__ = "UserRole"
  userRoleId = Column(Integer, primary_key = True, autoincrement = True)
  userId = Column(ForeignKey("User.userId"), nullable = False)
  roleId = Column(ForeignKey("Role.roleId"), nullable = False)

class Container(Base):
  __tablename__ = "Container"
  containerId = Column(Integer, primary_key = True, autoincrement = True)
  imageName = Column(String, unique = True, nullable = False)
  name = Column(String, nullable = False)
  description = Column(String, nullable = True)
  createdAt = Column(DateTime, nullable = False)
  ReservedContainers = relationship("ReservedContainer", back_populates = "Container")

class ReservedContainer(Base):
  __tablename__ = "ReservedContainer"
  reservedContainerId = Column(Integer, primary_key = True, autoincrement = True)
  containerId = Column(ForeignKey("Container.containerId"), nullable = False)
  startedAt = Column(DateTime, nullable = True)
  stoppedAt = Column(DateTime, nullable = True)
  status = Column(String, nullable = True)
  dockerContainerId = Column(String)
  sshPassword = Column(String, nullable = False)
  container = relationship("Container", back_populates = "ReservedContainer")

class Reservation(Base):
  __tablename__ = "Reservation"
  reservationId = Column(Integer, primary_key = True, autoincrement = True)
  reservedContainerId = Column(ForeignKey("ReservedContainer.reservedContainerId"), nullable = False)
  userId = Column(ForeignKey("User.userId"), nullable = False)
  startDate = Column(DateTime, nullable = False)
  endDate = Column(DateTime, nullable = False)
  createdAt = Column(DateTime, nullable = False)
  user = relationship("User", back_populates = "Reservation")
  reservedContainer = relationship("ReservedContainer", back_populates = "Reservation")
  reservedHardwareSpecs = relationship("HardwareSpec", secondary = "ReservedHardwareSpec", back_populates = "Reservation", single_parent = True)

class Computer(Base):
  __tablename__ = "Computer"
  computerId = Column(Integer, primary_key = True, autoincrement = True)
  name = Column(String, nullable = False, unique = True)
  createdAt = Column(DateTime, nullable = False)
  hardwareSpecs = relationship("HardwareSpec", back_populates = "Computer")

class HardwareSpec(Base):
  __tablename__ = "HardwareSpec"
  hardwareSpecId = Column(Integer, primary_key = True, autoincrement = True)
  computerId = Column(ForeignKey("Computer.computerId"), nullable = False)
  type = Column(String, nullable = False)
  maximumAmount = Column(Float, nullable = False)
  maximumAmountForUser = Column(Float, nullable = False)
  defaultAmountForUser = Column(Float, nullable = False)
  format = Column(String, nullable = False)
  computer = relationship("Computer", back_populates = "HardwareSpec")
  reservations = relationship("Reservation", secondary = "ReservedHardwareSpec", back_populates = "HardwareSpec", single_parent = True)

class ReservedHardwareSpec(Base):
  __tablename__ = "ReservedHardwareSpec"
  reservedHardwareSpecId = Column(Integer, primary_key = True, autoincrement = True)
  reservationId = Column(ForeignKey("Reservation.reservationId"), nullable = False)
  hardwareSpecId = Column(ForeignKey("HardwareSpec.hardwareSpecId"), nullable = False)
  UniqueConstraint('reservationId', 'hardwareSpecId', name='uniqueHardwareSpec')

# Create the tables
Base.metadata.create_all(engine)

# Create session to interact with the database
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()