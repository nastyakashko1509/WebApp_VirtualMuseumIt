from museum_parts.models import Ticket, Purchase, Exhibition, Hall, Exhibit, Tour
from django.db.models import Count, Sum, ExpressionWrapper, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractYear
from museum_information.models import PromoCode
from datetime import timedelta, date, datetime
from django.utils.timezone import now
from django.utils import timezone
from datetime import date
from .models import * 
import calendar
import pytz


# СТРАНИЦЫ "СПИСОК СОТРУДНИКОВ"

@login_required
def employee_list(request):

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

    return render(request, 'employee.html', {'employees': employees})


@login_required
def employee_detail(request, employee_id):

    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})


# СТРАНИЦЫ КЛИЕНТА/СОТРУДНИКА/АДМИНА

@login_required
def employee_dashboard(request):

    user_tz = pytz.timezone('Europe/Minsk')
    user = request.user
    employee = user.museum_employee

    now_utc = now()
    now_local = now_utc.astimezone(user_tz)
    today = now_local.date()

    cal = calendar.TextCalendar(calendar.MONDAY).formatmonth(now_local.year, now_local.month)

    exhibitions = Exhibition.objects.filter(responsible_employee=employee)

    exhibitions_data = []
    for exhibition in exhibitions:
        start_time_utc = exhibition.start_date.strftime('%d/%m/%Y %H:%M')
        end_time_utc = exhibition.end_date.strftime('%d/%m/%Y %H:%M')
        start_time_local = exhibition.start_date.astimezone(user_tz).strftime('%d/%m/%Y %H:%M')
        end_time_local = exhibition.end_date.astimezone(user_tz).strftime('%d/%m/%Y %H:%M')
        exhibitions_data.append({
            'title': exhibition.title,
            'exposition_description': [exp.name for exp in exhibition.exposition.all()],
            'start_time_utc': start_time_utc,
            'end_time_utc': end_time_utc,
            'start_time_local': start_time_local,
            'end_time_local': end_time_local,
        })

    tours = employee.tours.all()
    tours_data = []
    for tour in tours:
        start_time_utc = tour.start_time.strftime('%d/%m/%Y %H:%M') if tour.start_time else ''
        end_time_utc = tour.end_time.strftime('%d/%m/%Y %H:%M') if tour.end_time else ''
        start_time_local = tour.start_time.astimezone(user_tz).strftime('%d/%m/%Y %H:%M') if tour.start_time else ''
        end_time_local = tour.end_time.astimezone(user_tz).strftime('%d/%m/%Y %H:%M') if tour.end_time else ''
        tours_data.append({
            'tour': tour,
            'start_time_utc': start_time_utc,
            'end_time_utc': end_time_utc,
            'start_time_local': start_time_local,
            'end_time_local': end_time_local,
        })

    return render(request, 'employee_dashboard.html', {
        'employee': employee,
        'exhibitions': exhibitions_data,
        'tours_data': tours_data,
        'user_timezone': user_tz.zone,
        'current_date': now_local.strftime('%d/%m/%Y'),
        'calendar_text': cal,
    })


@login_required
def client_dashboard(request):

    user_tz = pytz.timezone('Europe/Minsk')
    client = request.user.museum_client
    today = now().date()
    now_utc = timezone.now()
    now_local = now_utc.astimezone(user_tz)
    today = now_local.date()

    promo_codes = PromoCode.objects.filter(is_active=True, valid_until__gte=today)
    tickets = Ticket.objects.all()
    purchases = Purchase.objects.filter(client=client).order_by('-purchase_date')

    cal = calendar.TextCalendar(calendar.MONDAY).formatmonth(now_local.year, now_local.month)

    purchases_data = []
    for purchase in purchases:
        purchases_data.append({
            'ticket': purchase.ticket,
            'purchase_date_utc': purchase.purchase_date.strftime('%d/%m/%Y %H:%M'),
            'purchase_date_local': purchase.purchase_date.astimezone(user_tz).strftime('%d/%m/%Y %H:%M'),
        })

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = Ticket.objects.filter(id=ticket_id).first()
        if ticket:
            Purchase.objects.create(client=client, ticket=ticket)
            return redirect('client_dashboard')

    return render(request, 'client_dashboard.html', {
        'client': client,
        'promo_codes': promo_codes,
        'tickets': tickets,
        'purchases': purchases,
        'purchases': purchases_data,
        'user_timezone': user_tz.zone,
        'current_date': now_local.strftime('%d/%m/%Y'),
        'calendar_text': cal,
    })


def get_season_months(season):
    return {
        'весна': (3, 4, 5),
        'лето': (6, 7, 8),
        'осень': (9, 10, 11),
        'зима': (12, 1, 2),
    }.get(season.lower(), (1, 2, 3))  


@login_required
def admin_dashboard(request):

    halls = Hall.objects.all()
    floor = request.GET.get("floor")
    employees = []
    if floor is not None:
        try:
            floor_int = int(floor)
            employees = Employee.objects.filter(halls__floor=floor_int).distinct()
        except ValueError:
            employees = []
    
    six_months_ago = date.today() - timedelta(days=180)
    new_exhibits = Exhibit.objects.filter(creation_date__gte=six_months_ago)
    all_exhibits = Exhibit.objects.all()

    show_new = request.GET.get('new') == '1'
    exhibits = new_exhibits if show_new else all_exhibits

    season = request.GET.get('season', 'лето').lower()
    season_months = get_season_months(season)

    tours = Tour.objects.filter(start_time__month__in=season_months)
    total_group_size = tours.aggregate(total_group=Sum('group_size'))['total_group'] or 0

    date_str = request.GET.get('date')
    exhibitions_count_by_hall = {}

    if date_str:
        try:
            date_filter = datetime.strptime(date_str, '%Y-%m-%d').date()
            exhibitions_count = Exhibition.objects.filter(
                start_date__gt=date_filter
            ).values('hall__id', 'hall__name').annotate(count=Count('id'))
            
            exhibitions_count_by_hall = {item['hall__id']: item['count'] for item in exhibitions_count}
            
        except ValueError:
            date_filter = None
    else:
        date_filter = None

    context = {
        'halls': halls,
        'exhibits': exhibits,
        'show_new': show_new,
        'employees': employees,
        'floor': floor,
        'tours': tours,
        'total_group_size': total_group_size,
        'selected_season': season,
        'exhibitions_count_by_hall': exhibitions_count_by_hall,
        'date_filter': date_str,
    }
    return render(request, 'admin_dashboard.html', context)
