from django.db import models
from django.utils import timezone  


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SliderSettings(models.Model):
    delay = models.IntegerField(default=5, verbose_name="Задержка между слайдами (сек)")
    loop = models.BooleanField(default=True, verbose_name="Зациклить слайдер")
    show_navs = models.BooleanField(default=True, verbose_name="Показывать стрелки")
    show_pagination = models.BooleanField(default=True, verbose_name="Показывать пагинацию")
    auto_play = models.BooleanField(default=True, verbose_name="Автопереключение")
    stop_on_hover = models.BooleanField(default=True, verbose_name="Останавливать при наведении")
    
    class Meta:
        verbose_name = "Настройка слайдера"
        verbose_name_plural = "Настройки слайдера"
