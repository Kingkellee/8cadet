import random
import shutil # for filesystem cleanup
from os.path import isdir # to check if directory exists
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250, default="Sample Album Photos")
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Albums"
        ordering = ("-creation_date",)

    def item_count(self):
        n = Picture.objects.filter(album__name=self.name).count()
        if n > 1:
            return f"{n} items."
        elif n == 1:
            return "1 item."
        return "Empty album."

    def random_image(self):
        lst = Picture.objects.filter(album__name=self.name)
        if lst:
            return random.choice(lst).picture
        return None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("gallery:single_album", kwargs={"album_name": self.name})

    def delete(self, *args, **kwargs):
        """Custom delete method to remove album directory once the album no longer exists in db"""
        
        location = settings.MEDIA_ROOT + "/" + self.name # location of album in the filesystem
        if isdir(location):
            shutil.rmtree(location)
        super().delete(*args, **kwargs)


def album_name(instance, filename):
    """Callable for upload_to argument in picture attribute below"""
    return f"gallery/{instance.album.name}/{filename}"


class Picture(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="pictures")
    picture = models.ImageField(upload_to=album_name, default="blank/no_img.png")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    description = models.CharField(max_length=500)

    # tags mechanism
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse(
            "gallery:single_picture",
            kwargs={"album_name": self.album.name, "pk": self.pk},
        )

    def delete(self, *args, **kwargs):
        """Custom delete method to remove pictures references not only from db, 
        but also from the filesystem"""

        self.picture.delete()
        super().delete(*args, **kwargs)

    
