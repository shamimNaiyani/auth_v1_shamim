from django.db import models
# you can use translation for location based language. E.g. if users will use this app fron Russia the fields name will translated into russian ! 
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}): {self.message[:20]}"
