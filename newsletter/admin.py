from django.contrib import admin
from .models import NewsletterList


class NewsletterListAdmin(admin.ModelAdmin):
	list_display = ('email', 'created')
	list_filter = ("email",)
	search_fields = ['email',]
	date_hierarchy = 'created'
  

admin.site.register(NewsletterList, NewsletterListAdmin)

# Register your models here.
