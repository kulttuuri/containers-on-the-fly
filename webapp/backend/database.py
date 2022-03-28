from sqlalchemy import create_engine
from settings import settings
engine = create_engine(settings.database["engineUri"] + settings.database["filePath"], echo=settings.database["debugPrinting"], future=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# Model for user
class User(Base):
  __tablename__ = "User"
  userId = Column(Integer, primary_key = True, autoincrement = True)
  email = Column(String, nullable = False)
  password = Column(String, nullable = False)

# Create the tables
Base.metadata.create_all(engine)

# Create session to interact with the database
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()