# User whitelisting table management functionality
from click import password_option
from database import UserWhitelist, session

def viewAll(opt_filter = None):
    '''
    Get all users from UserWhitelist
    Make a list and append all those users into the list
    Return the list
    '''
    all_whitelisted_users = session.query(UserWhitelist)
    all_whitelisted_users_list = []
    for user in all_whitelisted_users:
        all_whitelisted_users_list.append(user)
    return all_whitelisted_users_list



def addToWhitelist(emails_to_input, emails):
    '''
    Checks if the user with the given email already exists in the whitelist,
    If it doesn't then the email/emails get added.
    '''
    if session.query(UserWhitelist).filter(UserWhitelist.email == emails).first():
        print("User already exists in the whitelist!")
    else:
        print("Adding above email to whitelist")
        session.add(
            UserWhitelist(
                email = emails
            )
        )
        session.commit()



def removeFromWhitelist(emails_to_remove, emails):
    '''
    Checks if the email user is inputting is the same as the one in the whitelist,
    If emails are the same then remove it.
    And if the email wasn't found in the whitelist, then the user gets notified of that and nothing is removed.
    '''
    if session.query(UserWhitelist).filter(UserWhitelist.email == emails).first():
        print("Now deleting email from whitelist")
        session.query(UserWhitelist).filter(UserWhitelist.email == emails).delete()
        session.commit()    
    else:
        print("Email you are trying to remove is not in the whitelist!")
        
