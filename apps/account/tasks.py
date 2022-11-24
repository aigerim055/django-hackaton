from django.conf import settings
from config.celery import app
from django.core.mail import send_mail
from django.template.loader import render_to_string


@app.task
def send_activation_sms(phone, activation_code):
    from twilio.rest import Client
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'This is your activation code: {activation_code}',
        from_=settings.TWILIO_NUMBER,
        to=phone
    )
    print(message.sid)


@app.task
def send_activation_code(email, activation_code):
    activation_link = f'http://localhost:8000/account/activate/{activation_code}/'
    html_message = render_to_string(
        'account/code_mail.html',
        {'activation_link': activation_link}
        )
    send_mail(
        'activate your account!',
        '',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message,
        fail_silently=False   
    )