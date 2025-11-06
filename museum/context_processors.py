from museum_base.models import SliderSettings


def slider_settings(request):
    settings = SliderSettings.objects.first()
    if not settings:
        settings = SliderSettings.objects.create()
    return {'slider_settings': settings}
