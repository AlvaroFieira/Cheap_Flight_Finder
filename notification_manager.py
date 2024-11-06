from twilio.rest import Client
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()


class NotificationManager:

    @staticmethod
    def send_whatsapp(message_body):
        twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv("TWILIO_AUTH_TOKEN"))
        message = twilio_client.messages.create(
            from_=os.getenv('TWILIO_WHATSAPP_NUMBER'),
            body=message_body,
            to=os.getenv('TWILIO_VERIFIED_NUMBER')
        )

    @staticmethod
    def send_email(to_addrs, message_body):
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=os.getenv('SMTPLIB_FROM_EMAIL'), password=os.getenv('SMTPLIB_PASSWORD'))
            connection.sendmail(
                from_addr=os.getenv('SMTPLIB_FROM_EMAIL'),
                to_addrs=to_addrs,
                msg=f"Subject:New Low Price Flight!\n\n{message_body}".encode('utf-8')
            )
