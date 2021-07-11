from django.utils.translation import gettext as _
from django.db import models
from PIL import Image
from django_resized import ResizedImageField
import datetime
from django.utils.safestring import mark_safe




class ContactUs (models.Model):
	name = models.CharField(max_length=150, help_text="Enter your full name.")
	email = models.EmailField()
	subject = models.CharField(max_length=150)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Contact Us"

	def __str__(self):
		return self.name + "-" + self.email


YEAR_CHOICES = []
for y in range(2013, (datetime.datetime.now().year+1)):
	YEAR_CHOICES.append((y, y))


def current_year():
	return datetime.datetime.now().year


class Leaders (models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	other_name = models.CharField(max_length=255, blank=True, null=True)
	avatar = ResizedImageField(
    	size=[300, 300], 
    	crop=['middle', 'center'], 
    	quality=90, 
    	keep_meta=False, 
    	verbose_name='profile_pic',
    	default ='default.jpg',
    	upload_to='leaders', 
    	force_format='JPEG'
    )
	start_date = models.IntegerField(_('start_date'), choices=YEAR_CHOICES, default=current_year)
	end_date = models.IntegerField(_('end_date'),  choices=YEAR_CHOICES, default=current_year)
	achievement = models.TextField()

	def __str__(self):
		return self.first_name

	def avatar_tag(self):
		# img = Leaders.objects.get(id=self.avatar)
		if self.avatar is not None:
			return mark_safe('<img src="{}" height="50" />'.format(self.avatar.url))
		else:
			return ""

	def save(self, *args, **kwargs):

		if self.id and self.avatar:
			current_avatar = Leaders.objects.get(pk=self.id).avatar
			if current_avatar != self.avatar:
				current_avatar.delete()
		super(Leaders, self).save(*args, **kwargs)

	class Meta:
		ordering = ('-start_date',)
		verbose_name = "Leader"
		verbose_name_plural = "Leaders"


class Patron (models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	other_name = models.CharField(max_length=255, blank=True, null=True)
	avatar = ResizedImageField(
    	size=[300, 300], 
    	crop=['middle', 'center'], 
    	quality=90, 
    	keep_meta=False, 
    	verbose_name='profile_pic',
    	default ='default.jpg',
    	upload_to='patrons', 
    	force_format='JPEG'
    )
	start_date = models.IntegerField(_('start_date'), choices=YEAR_CHOICES, default=current_year)
	end_date = models.IntegerField(_('end_date'), choices=YEAR_CHOICES, default=current_year)
	contribution = models.TextField()

	def __str__(self):
		return self.first_name
	
	def avatar_tag(self):
		img = Patron.objects.get(avatar=self.avatar)
		if img.id is not None:
			return mark_safe('<img src="{}" height="50" />'.format(img.avatar.url))
		else:
			return ""

	def save(self, *args, **kwargs):

		if self.id and self.avatar:
			current_avatar = Patron.objects.get(pk=self.id).avatar
			if current_avatar != self.avatar:
				current_avatar.delete()
		super(Patron, self).save(*args, **kwargs)

	class Meta:
		ordering = ('-start_date',)
		verbose_name_plural = "Patrons"