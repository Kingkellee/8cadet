from django import forms
from .models import NewsletterList


class SubscriptionForm(forms.ModelForm):

	email = forms.EmailField(widget = forms.TextInput(attrs={
		"type": "email",
		"name": "name",
		"id": "email",
		"placeholder": "Enter your email address",
		"aria-label": "email address",
		"aria-describedby": "button-addon2",
		}), label=""
	)	
	
	class Meta:
		model = NewsletterList
		fields = ('email',)

	def __init__(self, *args, **kwargs):
	    super(SubscriptionForm, self).__init__(*args, **kwargs)

	    self.fields['email'].widget.attrs['class'] = 'form-control'
