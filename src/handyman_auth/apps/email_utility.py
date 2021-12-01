"""
Script for sending emails
"""

from django.core.mail import send_mail
from django.conf import settings
import smtplib

# import mimetypes
import email
import email.mime.application

from sentry_sdk.api import capture_exception


def send_email(
    recipient_list, send_attach=None, attach_path=None, subject=None, message=None
) -> str:

    """
    function to send emails
    """
    email_from = settings.EMAIL_HOST_USER
    email_pass = settings.EMAIL_HOST_PASSWORD
    try:
        if send_attach == True:

            msg = email.mime.multipart.MIMEMultipart()
            msg["Subject"] = "Handy Man Attachment"
            msg["From"] = "handyman@handyman.com"
            msg["To"] = str(recipient_list[0])

            txt = email.mime.text.MIMEText("Message")
            msg.attach(txt)
            ebook_dir = attach_path

            filename = ebook_dir
            fo = open(filename, "rb")
            file = email.mime.application.MIMEApplication(fo.read(), _subtype="pdf")
            fo.close()
            file.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(file)

            # smtp cofig
            s = smtplib.SMTP("smtp.gmail.com")
            s.starttls()
            s.login(email_from, email_pass)
            s.sendmail(email_from, recipient_list, msg.as_string())
            s.quit()
        else:
            send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        capture_exception(e)

    return f"{subject} email sent"
