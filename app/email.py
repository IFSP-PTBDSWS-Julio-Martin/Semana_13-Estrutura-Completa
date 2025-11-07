from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import requests
from datetime import datetime

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])    
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_simple_message(to, subject, newUser):
    message = Mail(
        from_email=app.config['API_FROM'],
        to_emails=to,
        subject= app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        html_content="Novo usuário cadastrado: " + newUser)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        # sg.set_sendgrid_data_residency("eu")
        # uncomment the above line if you are sending mail using a regional EU subuser
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
