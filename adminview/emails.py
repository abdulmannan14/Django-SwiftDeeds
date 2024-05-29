from threading import Thread
import json
import requests
from django.urls import reverse
from get_set_work.settings import ADMIN_EMAILS

# from . import models as result_models, utils as result_utils
FROM_EMAIL = "hello@swiftdeeds.com"
SENDER_NAME = "SwiftDeeds"


def purchased_product_payload(email):
    return {
        "from": {
            "email": FROM_EMAIL
        },
        "personalizations": [
            {
                "to": [
                    {
                        "email": email
                    }
                ],
                "dynamic_template_data": {

                }
            }
        ],
        "template_id": "d-f9c715d87075432881b5de901ea0f298"
    }


def approved_payload(email):
    return {
        "from": {
            "email": FROM_EMAIL
        },
        "personalizations": [
            {
                "to": [
                    {
                        "email": email
                    }
                ],
                "dynamic_template_data": {

                }
            }
        ],
        "template_id": "d-e67330205e1a4b2184f3e59f588df4d7"
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
        "template_id": " d-e67330205e1a4b2184f3e59f588df4d7"
    }


def send_email(email, final=None):
    print("sending eamil to {}".format(email))
    if final:
        print("sending eamil to {}     final----".format(email))
        payload = approved_payload(email)
    else:
        payload = purchased_product_payload(email)
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
