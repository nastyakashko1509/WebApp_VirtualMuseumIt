from django.contrib.auth.models import User as AdmUser
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from museum_base.models import *
from django.db import models
import re


class Client(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='museum_client')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    money = models.IntegerField(null=True, default=1000)
    tickets = models.ManyToManyField(
        'museum_parts.Ticket',
        through='ClientTicket',
        related_name='clients'
    )

    def clean(self):
        super().clean()  

        if self.phone:
            pattern = r'^\+375 \((25|29|33|44)\) \d{3}-\d{2}-\d{2}$'
            if not re.match(pattern, self.phone):
                raise ValidationError({
                    'phone': 'Номер телефона должен быть в формате +375 (29) XXX-XX-XX'
                })
            
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        if age < 18:
            raise ValidationError("Возраст клиента должен быть не менее 18 лет.")


class ClientTicket(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    ticket = models.ForeignKey('museum_parts.Ticket', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} купил {self.quantity} × {self.ticket.name}"


class Position(BaseModel):  
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title   


class Employee(BaseModel): 
    user = models.OneToOneField(AdmUser, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='museum_employee')
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    bio = models.TextField()
    photo = models.ImageField(upload_to='photos/employees/', default=None, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name="employees", blank=True)
    halls = models.ManyToManyField('museum_parts.Hall', related_name="employees", null=True, blank=True)
    work_description = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.full_name}"
    
    def clean(self):
        super().clean()  

        if self.phone:
            pattern = r'^\+375 \((25|29|33|44)\) \d{3}-\d{2}-\d{2}$'
            if not re.match(pattern, self.phone):
                raise ValidationError({
                    'phone': 'Номер телефона должен быть в формате +375 (29) XXX-XX-XX'
                })
            
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        if age < 18:
            raise ValidationError("Возраст сотрудника должен быть не менее 18 лет.")
    