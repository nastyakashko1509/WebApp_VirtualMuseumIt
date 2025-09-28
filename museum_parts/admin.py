from django.contrib import admin
from .models import *


models = (
    Hall, ArtType, Ticket, Cart,
    Exhibit, Exposition, Exhibition)

admin.site.register(Hall)
admin.site.register(ArtType)
admin.site.register(Ticket)
admin.site.register(Cart)
admin.site.register(Exhibit)
admin.site.register(Exposition)
admin.site.register(Exhibition)
admin.site.register(Purchase)
admin.site.register(Tour)
admin.site.register(PartnerCompanies)
