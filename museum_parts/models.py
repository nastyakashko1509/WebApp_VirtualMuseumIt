from museum_users.models import Client, Employee
from django.contrib.auth.models import User
from museum_base.models import *
from django.db import models


class Hall(BaseModel):  
    name = models.CharField(max_length=50)
    floor = models.IntegerField()
    square = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.name} (этаж {self.floor})"


class ArtType(BaseModel):  
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Ticket(BaseModel):
    name = models.CharField(null=True, blank=True, max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    AGE_CHOICES = [
        ('baby', '0-5 лет'),
        ('child', '5-18 лет'),
        ('adult', 'от 18 лет'),
    ]
    visitor_age = models.CharField(choices=AGE_CHOICES)
    DAY_CHOICES = [
        ('weekday', 'Будний день'),
        ('weekend', 'Выходной'),
        ('holiday', 'Праздник'),
    ]
    day_type = models.CharField(max_length=10, choices=DAY_CHOICES)
    photo_permission_fee = models.BooleanField(default=False)

    def __str__(self):
        return f'Билет ({self.get_day_type_display()}) - {self.price}₽ + Фото: {self.photo_permission_fee}₽'


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} - {self.ticket.name or "Билет"}'
    

class Exhibit(BaseModel):  
    title = models.CharField(max_length=200)
    description = models.TextField()
    art_type = models.ForeignKey(ArtType, on_delete=models.SET_NULL, null=True)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateField()
    author = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='photos/exhibits/')

    def __str__(self):
        return self.title
    

class Exposition(BaseModel):  
    name = models.CharField(max_length=200)
    description = models.TextField()
    exhibits = models.ManyToManyField(Exhibit, related_name="expositions")

    def __str__(self):
        return self.name


class Exhibition(BaseModel):  
    title = models.CharField(max_length=200)
    exposition = models.ManyToManyField(Exposition)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, related_name='exhibitions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    responsible_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='exhibitions')
    ticket = models.ManyToManyField(Ticket, related_name='exhibitions')

    def __str__(self):
        return self.title
    

class PartnerCompanies(BaseModel):  
    name = models.CharField(max_length=50)
    photo_logo = models.ImageField(upload_to='photos/partners/')
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name="Сайт компании")

    def __str__(self):
        return f"{self.name}"
    

class Purchase(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='purchases')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} - {self.ticket} ({self.purchase_date.strftime('%Y-%m-%d %H:%M')})"
    

class Tour(BaseModel):  
    title = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    responsible_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='tours')
    exhibitions = models.ManyToManyField(Exhibition, related_name='tours')
    ticket = models.ManyToManyField(Ticket, related_name='tours')
    group_size = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    