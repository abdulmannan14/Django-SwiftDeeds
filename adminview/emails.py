from threading import Thread
import json
import requests
from django.urls import reverse
from get_set_work.settings import ADMIN_EMAILS

# from . import models as result_models, utils as result_utils
FROM_EMAIL = "mannanmaan1425@gmail.com"
SENDER_NAME = "Get Set Work"


def get_register_payload(link, userprofile):
    return {
        "from": {
            "email": FROM_EMAIL
        },
        "personalizations": [
            {
                "to": [
                    {
                        "email": userprofile.user.email
                    }
                ],
                "dynamic_template_data": {
                    "username": userprofile.user.get_full_name(),
                    "url": link,
                    "receipt": True,
                }
            }
        ],
        "template_id": "d-f9c715d87075432881b5de901ea0f298"
    }


def get_resend_verification_payload(link, userprofile):
    return {
        "from": {
            "email": FROM_EMAIL
        },
        "personalizations": [
            {
                "to": [
                    {
                        "email": userprofile.user.email
                    }
                ],
                "dynamic_template_data": {
                    "username": userprofile.user.get_full_name(),
                    "url": link,
                    "receipt": True,
                }
            }
        ],
        "template_id": "d-8c8da8a10a534a58b591052147ef1713"
    }


def send_email(userprofile, base_url, type):
    print("sending eamil to {}".format(userprofile.user.email))
    url = "{}{}".format(base_url, reverse("verify-email", kwargs={"pk": userprofile.user.id}))
    payload = None
    if type == 'register':
        payload = get_register_payload(url, userprofile)
    elif type == 'resend verification':
        payload = get_resend_verification_payload(url, userprofile)
    elif type == 'new job':
        payload = get_register_payload(url, userprofile)
    payload = json.dumps(payload)
    headers = {
        'Authorization': 'Bearer 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',
        'Content-Type': 'application/json'
    }
    url = "https://api.sendgrid.com/v3/mail/send"
    response = requests.request("POST", url, headers=headers, data=payload)
    print("======SENT=======")
    return response


def async_emails(base_url, queryset):
    t = Thread(target=send_mass_emails, args=[base_url, queryset])
    t.daemon = True
    t.start()


def send_mass_emails(base_url: str, queryset):
    for result in queryset:
        send_email(result, base_url, 'register')
