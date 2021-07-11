from django.contrib import admin
from .models import ContactUs, Leaders, Patron


class ContactUsAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'message', 'date')
	list_filter = ("email",)
	search_fields = ['name', 'email']
	date_hierarchy = 'date'

class LeadersAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name', 'other_name', 'start_date', 'end_date', 'achievement', 'avatar_tag')
	list_filter = ("start_date",)
	search_fields = ['last_name', 'first_name']


class PatronAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name', 'other_name', 'start_date', 'end_date', 'contribution', 'avatar_tag')
	list_filter = ("start_date",)
	search_fields = ['last_name', 'first_name']


admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Leaders, LeadersAdmin)
admin.site.register(Patron, PatronAdmin)
