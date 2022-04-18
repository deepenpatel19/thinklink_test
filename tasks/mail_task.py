from flask_mail import Mail
from flask_mail import Message
import os


mail = None


def mail_initialization(app=None):
    global mail
    mail = Mail()
    mail.init_app(app)


def send_email():
    global mail
    msg = Message(
        sender=os.environ.get("email"),
        recipients=[os.environ.get("email")],
        body="BTC price lower or higher than mentioned.",
        subject="Email regarding BTC price."
    )
    mail.send(msg)
