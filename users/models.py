from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from PIL import Image
from django_resized import ResizedImageField


class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	reg_no = models.CharField(max_length = 50, null=True, blank =True, default=None)
	status = models.CharField(max_length = 280, blank =True)
	bio = models.TextField()
	avatar = ResizedImageField(
    	size=[300, 300], 
    	crop=['middle', 'center'], 
    	quality=90, 
    	keep_meta=False, 
    	verbose_name='profile_pic',
    	default ='default.jpg',
    	upload_to='profile_pics', 
    	force_format='JPEG'
    )
	website_url = models.CharField(max_length=200, null=True, blank=True)
	facebook_url = models.CharField(max_length=200, null=True, blank=True)
	twitter_url = models.CharField(max_length=200, null=True, blank=True)
	instagram_url = models.CharField(max_length=200, null=True, blank=True)
	whatsapp_url = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return str(self.user)

	def save(self, *args, **kwargs):
		if self.id and self.avatar:
			current_avatar = Profile.objects.get(pk=self.id).avatar
			if current_avatar != self.avatar:
				current_avatar.delete()

		if self.reg_no is None:
			number = get_random_string(8, allowed_chars='0123456789')
			reg_id = '8BG/{}/{}'.format(timezone.now().strftime('%y'), number)
			self.reg_no = reg_id
		

		super(Profile, self).save(*args, **kwargs)

	# def create_reg_no(self):
	# 	number = get_random_string(8, allowed_chars='0123456789')
	# 	reg_no = '8BG/{}/{}'.format(timezone.now().strftime('%y'), number)
	# 	self.reg_no = reg_no


	def get_absolute_url(self):
		return reverse("profile_page")

    # delete profile img too
	def delete(self, *args, **kwargs):
		self.image.delete()
		return super(Profile, self).delete(*args, **kwargs)