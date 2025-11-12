from museum_parts.models import Tour, Hall, Exhibition, Exposition, PartnerCompanies
from django.db.models import ExpressionWrapper, IntegerField
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractYear
from museum_users.models import Employee
from museum_information.models import *
from django.http import JsonResponse
from django.shortcuts import render
from datetime import date
import time


def home(request):
    last_news = News.objects.order_by('-published_at').first()
    return render(request, 'home.html', {'last_news': last_news})


def toys_view(request):
    return render(request, 'toys.html')


def checkbox_generator(request):
    return render(request, 'checkbox_generator.html')


@login_required
def employee_task3(request):

    employees = Employee.objects.all()

    search_age = request.GET.get('age')
    sort_by = request.GET.get('sort')
    current_year = date.today().year

    employees = employees.annotate(
        birth_year=ExtractYear('date_of_birth'),
        age=ExpressionWrapper(
            current_year - ExtractYear('date_of_birth'),
            output_field=IntegerField()
        )
    )

    if search_age:
        try:
            search_age = int(search_age)
            employees = employees.filter(age=search_age)
        except ValueError: ...

    if sort_by == 'name':
        employees = employees.order_by('full_name')
    elif sort_by == 'age':
        employees = employees.order_by('age')

    return render(request, 'employee_task3.html', {'employees': employees})


def employees_api(request):
    time.sleep(3)

    employees = Employee.objects.select_related('position').all()
    data = []
    for emp in employees:
        data.append({
            'full_name': emp.full_name,
            'age': emp.age(),
            'position': emp.position.title if emp.position else '',
            'phone': emp.phone,
            'email': emp.email,
            'bio': emp.bio,
        })
    return JsonResponse(data, safe=False)


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
