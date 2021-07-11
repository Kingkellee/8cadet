from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import NewsletterList
from .forms import SubscriptionForm

import json
import requests

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_LIST_ID = settings.MAILCHIMP_EMAIL_LIST_ID

api_url = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
members_endpoint = f'{api_url}/lists/{MAILCHIMP_EMAIL_LIST_ID}/members'

def subscribe_email(email):
    data = {
        "email_address": email,
        "status": "subscribed"
    }

    req = requests.post(
        members_endpoint,
        auth=("", MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return req.status_code, req.json()


def subscription_list(request):

	form = SubscriptionForm(request.POST or None)
	if request.method == "POST":

		if form.is_valid():
			email_query = NewsletterList.objects.filter(email=form.instance.email)
			if email_query.exists():
				messages.info(request, "You are already subscribed to our mailing list")
			else:
				try:
					subscribe_email(form.instance.email)
					form.save()
					messages.success(request, "Your email has been added to our mailing list")
				except:
					messages.warning(request, "Something went wrong, try again!!")
					return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		else:
			messages.warning(request, "You didn't put an email address")
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
