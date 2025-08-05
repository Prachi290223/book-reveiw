from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):

    USER_TYPE=(
        ('admin','Admin'),
        ('normal','Normal user'),
    )
    user_type=models.CharField(max_length=100,choices=USER_TYPE,default='normal')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})"

class Books(models.Model):
   
    title=models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='books')
    book_description=models.TextField()
    genre=models.CharField(max_length=100)
    book_image=models.ImageField(upload_to="book_image/",blank=True, null=True)
    
    def average_rating(self):
        return 0
        
    def __str__(self):
        return self.title
   

class Review(models.Model):
    book=models.ForeignKey(Books,on_delete=models.CASCADE,related_name='reveiws')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reveiws')
    comment=models.TextField()
    rating=models.IntegerField()

    def __str__(self):
        return f"{self.user.username}{self.book.title}"