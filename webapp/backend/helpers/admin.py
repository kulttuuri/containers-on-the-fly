from database import session, User, UserWhitelist, Role

# Admin utility functions

def whitelistUser(email: str):
  session.add(UserWhitelist(
    email = email
  ))
  session.commit()
  print("Whitelisted user: " + email)

def removeFromWhitelist(email: str):
  session.commit()
  session.query(UserWhitelist).filter( UserWhitelist.email == email ).delete()
  session.commit()
  print("Removed user from whitelist: " + email)

def makeUserAdmin(email: str):
  user = session.query(User).filter( User.email == email ).first()
  if user == None:
    print("No user found to be made as admin!")
    return
  adminRole = session.query(Role).filter( Role.name == "admin" ).first()
  user.roles.append(adminRole)
  session.commit()
  print("Made user admin: " + email)

def removeFromAdminRole(email: str):
  user = session.query(User).filter( User.email == email ).first()
  if user == None:
    print("No user found to be made as admin!")
    return
  for role in user.roles:
    if (role.name == "admin"): user.roles.remove(role)
    session.commit()
  print("Removed user from the admin role: " + email)