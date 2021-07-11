from django.db import models


class NewsletterList(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    
