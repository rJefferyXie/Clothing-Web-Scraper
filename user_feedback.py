# this is the start of user feedback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = "370scraper2020@gmail.com"
password = "ILoveScrapers"


def send_mail(to_emails=None):
    # to make sure to_emails is of type 'list'
    assert isinstance(to_emails, list)
    message = MIMEMultipart('alternative')
    # asking the user's input (single or multiple lines)
    user_email = input("Please enter your email: ")
    if user_email == "":
        from_email = "Anonymous <370scraper2020@gmail.com>"
    else:
        from_email = f"{user_email} <370scraper2020@gmail.com>"
        # asking the user for the email subject
    subject = input("Enter the subject: ")
    lines = []
    print("Enter your comment: ")
    while True:
        line = input()
        if line == "submit":
            break
        elif line:
            lines.append(line)
        elif not line:
            lines.append('\n')

    text = '\n'.join(lines)
    message['From'] = from_email
    message['To'] = ", ".join(to_emails)
    message['Subject'] = subject
    text_part = MIMEText(text, 'plain')
    message.attach(text_part)
    # html_part = MIMEText("<h1> This is working </h1>", 'html')
    message_string = message.as_string()
    # log in into my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    # this is default configuration
    server.ehlo()
    # this is to start the secured server
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, message_string)
    server.quit()


def send_mail_GUI(user_email, user_subject, user_message, to_emails=None):
    # to make sure to_emails is of type 'list'
    assert isinstance(to_emails, list)
    message = MIMEMultipart('alternative')
    # asking the user's input (single or multiple lines)
    email = user_email
    if email == "":
        from_email = "Anonymous <370scraper2020@gmail.com>"
    else:
        from_email = f"{email} <370scraper2020@gmail.com>"
        # asking the user for the email subject
    subject = user_subject
    text = user_message
    message['From'] = from_email
    message['To'] = ", ".join(to_emails)
    message['Subject'] = subject
    text_part = MIMEText(text, 'plain')
    message.attach(text_part)
    # html_part = MIMEText("<h1> This is working </h1>", 'html')
    message_string = message.as_string()
    # log in into my smtp server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    # this is default configuration
    server.ehlo()
    # this is to start the secured server
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, message_string)
    server.quit()


if __name__ == "__main__":
    send_mail(to_emails=["370scraper2020@gmail.com"])
