import os
import requests

def send_simple_message(to, send_from, subject, html):
    api_key = os.environ.get('MAILGUN_API')
    return requests.post(
        "https://api.mailgun.net/v3/mg.registerformass.com/messages",
        auth=("api", api_key),
        data={
            "from": send_from,
            "to": to,
            "subject": subject,
            "html": html
        })






