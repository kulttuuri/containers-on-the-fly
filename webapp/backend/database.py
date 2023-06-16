from sqlalchemy import create_engine
from settings import settings
import pymysql
engine = create_engine(settings.database["engineUri"] + settings.database["filePath"], echo=settings.database["debugPrinting"], future=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, Text, Float, ForeignKey, DateTime, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
  __tablename__ = "User"

  userId = Column(Integer, primary_key = True, autoincrement = True)
  email = Column(Text, nullable = False)
  password = Column(Text, nullable = True)
  passwordSalt = Column(Text, nullable = True)
  loginToken = Column(Text, nullable = True)
  loginTokenCreatedAt = Column(DateTime, nullable = True)
  userCreatedAt = Column(DateTime(timezone=True), server_default=func.now())
  userUpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  userStorage = relationship("UserStorage", back_populates = "user")
  roles = relationship("Role", secondary = "UserRole", back_populates = "users", single_parent=True)
  reservations = relationship("Reservation", back_populates = "user")

# If whitelisting is enabled, then only the email addresses specified here can login
class UserWhitelist(Base):
  __tablename__ = "UserWhitelist"

  userWhitelistId = Column(Integer, primary_key = True, autoincrement = True)
  email = Column(Text, nullable = True, unique = True)

class UserStorage(Base):
  __tablename__ = "UserStorage"

  userStorageId = Column(Integer, primary_key = True, autoincrement = True)
  userId = Column(ForeignKey('User.userId'), unique = True, nullable = False)
  #location = Column(Text, nullable = False) # TODO: Add to diagram
  maxSpace = Column(Float, nullable = False)
  maxSpaceFormat = Column(Text, nullable = False)
  UniqueConstraint('userStorageId', 'userId', name='uniqueUserStorage')
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  user = relationship("User", back_populates = "userStorage")

class Role(Base):
  __tablename__ = "Role"

  roleId = Column(Integer, primary_key = True, autoincrement = True)
  name = Column(Text, nullable = False, unique = True)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  users = relationship("User", secondary = "UserRole", back_populates = "roles", single_parent=True)

class UserRole(Base):
  __tablename__ = "UserRole"

  userRoleId = Column(Integer, primary_key = True, autoincrement = True)
  userId = Column(ForeignKey("User.userId"), nullable = False)
  roleId = Column(ForeignKey("Role.roleId"), nullable = False)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

class Container(Base):
  __tablename__ = "Container"

  containerId = Column(Integer, primary_key = True, autoincrement = True)
  public = Column(Boolean, nullable = False)
  imageName = Column(String, unique = True, nullable = False)
  name = Column(String, nullable = False)
  removed = Column(Boolean, nullable = True) # TODO: Add to diagram
  description = Column(String, nullable = True)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  reservedContainers = relationship("ReservedContainer", back_populates = "container")
  containerPorts = relationship("ContainerPort", back_populates = "container")

class ContainerPort(Base):
  __tablename__ = "ContainerPort"

  containerPortId = Column(Integer, primary_key = True, autoincrement = True)
  containerId = Column(ForeignKey("Container.containerId"), nullable = False)
  serviceName = Column(Text, nullable = False)
  port = Column(Integer, nullable = False)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  container = relationship("Container", back_populates = "containerPorts")
  reservedContainerPorts = relationship("ReservedContainerPort", back_populates = "containerPort")

class ReservedContainer(Base):
  __tablename__ = "ReservedContainer"

  reservedContainerId = Column(Integer, primary_key = True, autoincrement = True)
  containerId = Column(ForeignKey("Container.containerId"), nullable = False)
  startedAt = Column(DateTime, nullable = True)
  stoppedAt = Column(DateTime, nullable = True)
  containerDockerName = Column(Text, nullable = True) # Used for stopping the container
  containerStatus = Column(Text, nullable = True) # Coming from Docker
  containerDockerId = Column(Text, nullable = True) # Coming from Docker
  containerId = Column(ForeignKey("Container.containerId"), nullable = False)
  sshPassword = Column(Text, nullable = True)
  containerDockerErrorMessage = Column(Text, nullable = True)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  reservation = relationship("Reservation", back_populates = "reservedContainer")
  container = relationship("Container", back_populates = "reservedContainers")
  reservedContainerPorts = relationship("ReservedContainerPort", back_populates = "reservedContainer")

class ReservedContainerPort(Base):
  __tablename__ = "ReservedContainerPort"
  
  reservedContainerPortId = Column(Integer, primary_key = True, autoincrement = True)
  reservedContainerId = Column(ForeignKey("ReservedContainer.reservedContainerId"), nullable = False)
  containerPortForeign = Column(ForeignKey("ContainerPort.containerPortId"), nullable = False)
  outsidePort = Column(Integer, nullable = False)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
  UniqueConstraint('reservedContainerId', 'localPort', name='outsidePort')

  reservedContainer = relationship("ReservedContainer", back_populates = "reservedContainerPorts")
  containerPort = relationship("ContainerPort", back_populates = "reservedContainerPorts")

class Reservation(Base):
  __tablename__ = "Reservation"

  reservationId = Column(Integer, primary_key = True, autoincrement = True)
  reservedContainerId = Column(ForeignKey("ReservedContainer.reservedContainerId"), nullable = False)
  computerId = Column(ForeignKey("Computer.computerId"), nullable = False)
  userId = Column(ForeignKey("User.userId"), nullable = False)
  startDate = Column(DateTime, nullable = False)
  endDate = Column(DateTime, nullable = False)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
  status = Column(Text, nullable = False) # reserved, started, stopped, error

  user = relationship("User", back_populates = "reservations")
  reservedContainer = relationship("ReservedContainer", back_populates = "reservation")
  reservedHardwareSpecs = relationship("ReservedHardwareSpec", back_populates = "reservation")
  computer = relationship("Computer", back_populates = "reservations")

class Computer(Base):
  __tablename__ = "Computer"

  computerId = Column(Integer, primary_key = True, autoincrement = True)
  public = Column(Boolean, nullable = False)
  name = Column(Text, nullable = False, unique = True)
  ip = Column(Text, nullable = False)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  hardwareSpecs = relationship("HardwareSpec", back_populates = "computer")
  reservations = relationship("Reservation", back_populates = "computer")

class HardwareSpec(Base):
  __tablename__ = "HardwareSpec"

  hardwareSpecId = Column(Integer, primary_key = True, autoincrement = True)
  computerId = Column(ForeignKey("Computer.computerId"), nullable = False)
  internalId = Column(String, nullable = True) # TODO: Add to diagram
  type = Column(String, nullable = False)
  maximumAmount = Column(Float, nullable = False)
  minimumAmount = Column(Float, nullable = False)
  maximumAmountForUser = Column(Float, nullable = False)
  defaultAmountForUser = Column(Float, nullable = False)
  format = Column(Text, nullable = False)
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  computer = relationship("Computer", back_populates = "hardwareSpecs")
  reservations = relationship("ReservedHardwareSpec", back_populates = "hardwareSpec")

class ReservedHardwareSpec(Base):
  __tablename__ = "ReservedHardwareSpec"
  
  reservedHardwareSpecId = Column(Integer, primary_key = True, autoincrement = True)
  reservationId = Column(ForeignKey("Reservation.reservationId"), nullable = False)
  hardwareSpecId = Column(ForeignKey("HardwareSpec.hardwareSpecId"), nullable = False)
  amount = Column(Float, nullable = False)
  #UniqueConstraint('reservationId', 'hardwareSpecId', name='uniqueHardwareSpec')
  createdAt = Column(DateTime(timezone=True), server_default=func.now())
  updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

  hardwareSpec = relationship("HardwareSpec", back_populates = "reservations")
  reservation = relationship("Reservation", back_populates = "reservedHardwareSpecs")

# Create the tables
Base.metadata.create_all(engine)

# Create session to interact with the database
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)