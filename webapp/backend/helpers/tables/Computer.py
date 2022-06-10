# Computer table management functionality
from database import Computer, session

def getComputers(filter = None):
  '''
  Finds computers with the given optional filter. If no filter is given, finds all computers in the system.
    Parameters:
      filter: Additional filters. Example usage: ...
    Returns:
      All found computers in a list.
  '''
  if filter != None:
    computers = session.query(Computer).filter(Computer.name == filter).first()
    if computers != None: return [computers]
    else:
      try:
        computers = session.query(Computer).filter(Computer.computerId == int(filter)).first()
        if computers != None: return [computers]
        else: return None
      except:
        return None
  else: computers = session.query(Computer).all()
  return computers

def addComputer(name, public):
  '''
  Adds the given computer in the system.
    Parameters:
      name: The name of the computer to be added.
      public: Boolean. Whether the computer is public or not.
    Returns:
      The created computer object fetched from database. Or None if provided name already exists.
  '''
  duplicate = session.query(Computer).filter(Computer.name == name).first()
  if duplicate != None:
      return None
  newComputer = Computer(name = name, public = public)
  session.add(newComputer)
  session.commit()
  return session.query(Computer).filter(Computer.name == name).first()

def removeComputer(computer):
  '''
  Removes the given computer in the system.
    Parameters:
      computer: The computer object of the computer to be removed.
    Returns:
      Nothing
  '''
  session.delete(computer)
  session.commit()

def editComputer(computer, new_name = None, new_public = None):
  '''
  Edits the given computer in the system.
    Parameters:
      computer: The computer object of the computer to be edited.
      new_name: The new name for the given computer.
      new_public: The new boolean for publicity of the computer.
    Returns:
      The edited computer object fetched from database. Or None if name or publicity isn't provided.
  '''
  if new_name != None: computer.name = new_name
  if new_public != None: computer.public = new_public
  session.commit()
  return computer