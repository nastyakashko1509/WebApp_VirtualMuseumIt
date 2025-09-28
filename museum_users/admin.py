from django.contrib import admin
from .models import *


models = (Client, Position, Employee, ClientTicket)

admin.site.register(Client)
admin.site.register(ClientTicket)
admin.site.register(Position)
admin.site.register(Employee)
