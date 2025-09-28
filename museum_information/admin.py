from django.contrib import admin
from .models import *


models = (
    AboutCompany, FAQ, News,
    PromoCode, Review)

admin.site.register(AboutCompany)
admin.site.register(FAQ)
admin.site.register(News)
admin.site.register(PromoCode)
admin.site.register(Review)
