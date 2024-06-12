from django.db import models 
from django.contrib.auth.models import User 


# Create your model here 
class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2) 
    product_image=models.ImageField(upload_to="thumbnail") 
    book_url=models.URLField() 
    
    def __str__(self):
        return self.name 