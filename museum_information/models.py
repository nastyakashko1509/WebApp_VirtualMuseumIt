from django.contrib.auth.models import User
from museum_base.models import *
from django.db import models
import re


class AboutCompany(BaseModel):  
    content = models.TextField()

    def __str__(self):
        return self.content
    

class FAQ(BaseModel):  
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True, null=True)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question


class News(BaseModel):  
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='photos/news_images/')
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_first_sentence(self):
        match = re.search(r'^.*?[.!?]', self.content)
        if match:
            return match.group(0)
        else:
            words = self.content.split()
            if len(words) > 50:
                return ' '.join(words[:50]) + '...'
            return self.content


class PromoCode(BaseModel):  
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    valid_until = models.DateField()

    def __str__(self):
        return self.code
    

class Review(BaseModel):  
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} — {self.rating}/5"
