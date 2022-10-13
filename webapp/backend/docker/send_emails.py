#! /usr/bin/python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO Change password to file, that is not part of the repo
def send_email(to, mail_subject,mail_body,file=None):
    username = "samk.ailab@samk.fi"
    password = "F0Wypt0n7o"
    mail_from = "samk.ailab@samk.fi"

    mimemsg = MIMEMultipart()
    mimemsg['From']=mail_from
    mimemsg['To']=to
    mimemsg['Subject']=mail_subject
    mimemsg.attach(MIMEText(mail_body, 'plain'))
    try:    
        connection = smtplib.SMTP(host='smtp.office365.com', port=587)
        connection.starttls()
        connection.login(username,password)
        connection.send_message(mimemsg)
        connection.quit()
    except (smtplib.SMTPConnectError, smtplib.SMTPAuthenticationError) as e:
        print(f"something went wrong: {e}")

if __name__ == "__main__":
    send_email("toni.aaltonen@samk.fi","testing email from python","This is a test message", file=None)