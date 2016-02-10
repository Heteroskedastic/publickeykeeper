from flask.ext.mail import Message

from base import mail


def send_email(subject, recepients, body):
    if not isinstance(recepients, list):
        recepients = [recepients]
    msg = Message(subject,
                  sender="support@publickeykeeper.org",
                  recipients=recepients)
    msg.body = body
    mail.send(msg)
