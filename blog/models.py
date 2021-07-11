from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from django_resized import ResizedImageField
    

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)


    class Meta:
        verbose_name_plural =  "Categories"
     
    def __str__(self):
        return self.name

    
    def get_absolute_url(self):
        return reverse("category", kwargs={
            'id': self.id
        })


    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.capitalize()

        super(Category, self).save(*args, **kwargs)

        

STATUS = (
    (0, "Draft"),
    (1, "Publish"),
    
)


class Post (models.Model):
    title = models.CharField(max_length=200, unique=True)
    # header_image = models.ImageField(null=True, blank=True, upload_to='images/')
    slug = models.SlugField(max_length=200, unique=True)
    header_image = ResizedImageField(size=[900, 600], crop=['middle', 'center'], quality=90, keep_meta=False, upload_to='posts_image', default ='default.jpg', force_format='JPEG')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField(blank=True, null=True)
    # content = models.TextField()
    category = models.ManyToManyField(Category)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS,default = 0)
    featured = models.BooleanField(default=False)
    tags = TaggableManager()
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    

    class Meta:
        ordering = ['-created_on']
        
     
        
    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.header_image.delete()
        return super(Post, self).delete(*args, **kwargs)


    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug":str(self.slug)})

    @property
    def get_all_comments(self):
        return self.comments.all().order_by('created_on')

    @property
    def get_comments_count(self):
        return self.comments.all().count()


