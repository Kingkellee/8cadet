from django import forms
from .models import ContactUs, Leaders, Patron
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from crispy_forms.helper import FormHelper
from countable_field.widgets import CountableWidget
import datetime

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		fields ='__all__'


YEAR_CHOICES = []
for y in range(2013, (datetime.datetime.now().year+1)):
	YEAR_CHOICES.append((y, y))



class AddLeadersForm(forms.ModelForm):

	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),  label="")
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),  label="")
	other_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Name'}), required=False, label="")
	start_date = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=sorted(YEAR_CHOICES, key=lambda x:x[1], reverse=True),), label="")
	end_date = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=sorted(YEAR_CHOICES, key=lambda x:x[1], reverse=True),), label="")
	achievement = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List Achievements Here'}),  label="")

	def clean(self):
		cleaned_data = super(AddLeadersForm, self).clean()
		start_date = self.cleaned_data.get('start_date')
		end_date = self.cleaned_data.get('end_date')

		# all_leaders = Leaders.objects.all()
		if start_date:
			
			if Leaders.objects.filter(start_date=start_date).exists(): 
				raise forms.ValidationError('A Leader already exists with  start date {}, No two Leaders can have the same Start Date'.format(start_date))

		if end_date:
			if Leaders.objects.filter(end_date=end_date).exists():
				raise forms.ValidationError('A Leader already exists with end date {} No two Leaders can have the same End Date'.format(end_date))		

		if start_date >= end_date:
			raise forms.ValidationError('Start Date should not be greater than End Date')

	def __init__(self, *args, **kwargs):
		super(AddLeadersForm, self).__init__(*args, **kwargs)

		self.fields['achievement'].widget = CountableWidget(attrs={'data-min-count': 100, 'data-max-count': 200})
		self.fields['achievement'].help_text = "Must be between 100 and 200 words"
		self.helper = FormHelper(self)
		self.helper.help_text_inline = False		



	class Meta:
		model = Leaders
		fields = '__all__'
	

class AddPatronForm(forms.ModelForm):

	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),  label="")
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),  label="")
	other_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Name'}), required=False, label="")
	start_date = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=sorted(YEAR_CHOICES, key=lambda x:x[1], reverse=True),), label="")
	end_date = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=sorted(YEAR_CHOICES, key=lambda x:x[1], reverse=True),), label="")
	contribution = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List Contributions Here'}),  label="")
	
	def clean(self):
		cleaned_data = super(AddPatronForm, self).clean()
		start_date = self.cleaned_data.get('start_date')
		end_date = self.cleaned_data.get('end_date')

		if start_date:
			if Patron.objects.filter(start_date=start_date).exists(): 
				raise forms.ValidationError('A Patron already exists with start date {}, No two Leaders can have the same Start Date'.format(start_date))

		if end_date:
			if Patron.objects.filter(end_date=end_date).exists():
				raise forms.ValidationError('A Patron already exists with end date {} No two Leaders can have the same End Date'.format(end_date))		


		if start_date >= end_date:
			raise forms.ValidationError('Start Date should not be greater than End Date')

	class Meta:
		model = Patron
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(AddPatronForm, self).__init__(*args, **kwargs)

		self.fields['contribution'].widget = CountableWidget(attrs={'data-min-count': 100, 'data-max-count': 200})
		self.fields['contribution'].help_text = "Must be between 100 and 200 words"
		self.helper = FormHelper(self)
		self.helper.help_text_inline = False

class UpdateLeadersForm(forms.ModelForm):

	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),  label="")
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),  label="")
	other_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Name'}), required=False, label="")
	achievement = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List Achievements Here'}),  label="")


	class Meta:
		model = Leaders
		fields = ['first_name', 'last_name', 'other_name', 'avatar', 'achievement']


	def __init__(self, *args, **kwargs):
		super(UpdateLeadersForm, self).__init__(*args, **kwargs)

		self.fields['achievement'].widget = CountableWidget(attrs={'data-min-count': 100, 'data-max-count': 200})
		self.fields['achievement'].help_text = "Must be between 100 and 200 words"
		self.helper = FormHelper(self)
		self.helper.help_text_inline = False	

class UpdatePatronForm(forms.ModelForm):

	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),  label="")
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),  label="")
	other_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Other Name'}), required=False, label="")
	contribution = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List Contributions Here'}),  label="")
	

	class Meta:
		model = Patron
		fields = fields = ['first_name', 'last_name', 'other_name', 'avatar', 'contribution']


	def __init__(self, *args, **kwargs):
		super(UpdatePatronForm, self).__init__(*args, **kwargs)

		self.fields['contribution'].widget = CountableWidget(attrs={'data-min-count': 100, 'data-max-count': 200})
		self.fields['contribution'].help_text = "Must be between 100 and 200 words"
		self.helper = FormHelper(self)
		self.helper.help_text_inline = False



