from django.contrib import admin
from .models import SliderSettings

@admin.register(SliderSettings)
class SliderSettingsAdmin(admin.ModelAdmin):
    list_display = ['delay', 'loop', 'show_navs', 'show_pagination', 'auto_play', 'stop_on_hover']