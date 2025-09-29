from museum_parts.models import Tour, Hall, Exhibition, Exposition, PartnerCompanies
from django.contrib.auth.decorators import login_required
from museum_information.models import *
from django.shortcuts import render


def home(request):
    last_news = News.objects.order_by('-published_at').first()
    return render(request, 'home.html', {'last_news': last_news})


def museum_info(request):

    tours = Tour.objects.all()
    halls = Hall.objects.all()
    exhibitions = Exhibition.objects.all()
    expositions = Exposition.objects.all()
    promo_codes = PromoCode.objects.all()
    partners = PartnerCompanies.objects.all()

    return render(request, 'museum_info.html', {
        'tours': tours,
        'halls': halls,
        'exhibitions': exhibitions,
        'expositions': expositions,
        'promo_codes': promo_codes,
        'partners': partners
    })


def additional_page_view(request):
    return render(request, 'additional_page.html')
