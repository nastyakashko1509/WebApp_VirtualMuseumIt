from django.db.models import Sum, F, Case, When, Value, DecimalField
from statistics import mean, median, mode, StatisticsError
from museum_parts.models import Purchase
from museum_users.models import Client
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
import matplotlib.pyplot as plt
from collections import Counter
from io import BytesIO


def sales_by_visitor_age_chart(request):
    
    data = Purchase.objects.values('ticket__visitor_age').annotate(count=Count('id'))
    categories = [item['ticket__visitor_age'] for item in data]
    counts = [item['count'] for item in data]

    labels = {'baby': '0-5 лет', 'child': '5-18 лет', 'adult': 'от 18 лет'}
    labels_display = [labels.get(cat, cat) for cat in categories]

    plt.figure(figsize=(8, 5))
    plt.bar(labels_display, counts, color='sandybrown')
    plt.title('Продажи билетов по возрастным категориям')
    plt.xlabel('Возрастная категория')
    plt.ylabel('Количество продаж')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def sales_by_day_type_chart(request):

    data = Purchase.objects.values('ticket__day_type').annotate(count=Count('id'))
    categories = [item['ticket__day_type'] for item in data]
    counts = [item['count'] for item in data]

    labels = {'weekday': 'Будний день', 'weekend': 'Выходной', 'holiday': 'Праздник'}
    labels_display = [labels.get(cat, cat) for cat in categories]

    plt.figure(figsize=(8, 5))
    plt.pie(counts, labels=labels_display, autopct='%1.1f%%', startangle=140, colors=['#f4a261', '#e76f51', '#2a9d8f'])
    plt.title('Распределение продаж по типам дней')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def sales_over_time_chart(request):

    data = Purchase.objects.extra({'purchase_day': "date(purchase_date)"}).values('purchase_day').annotate(count=Count('id')).order_by('purchase_day')

    dates = [item['purchase_day'] for item in data]
    counts = [item['count'] for item in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, counts, marker='o', linestyle='-', color='steelblue')
    plt.title('Продажи билетов по дням')
    plt.xlabel('Дата')
    plt.ylabel('Количество продаж')
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def sales_charts_page(request):
    return render(request, 'sales_charts.html')


def statistics_view(request):

    clients = Client.objects.all().order_by('full_name')
    purchases = Purchase.objects.select_related('ticket').all()

    total_sales = Purchase.objects.annotate(
        full_price=F('ticket__price') + Case(
            When(ticket__photo_permission_fee=True, then=Value(5.00)),  
            default=Value(0.00),
            output_field=DecimalField()
        )
    ).aggregate(total=Sum('full_price'))['total'] or 0

    sales_amounts = [p.ticket.price for p in purchases]

    avg_sale = mean(sales_amounts) if sales_amounts else 0
    med_sale = median(sales_amounts) if sales_amounts else 0
    try:
        mode_sale = mode(sales_amounts) if sales_amounts else 0
    except StatisticsError:
        mode_sale = "Мода не определена (все значения уникальны)"

    today = timezone.now().date()
    client_ages = [
        today.year - client.date_of_birth.year - ((today.month, today.day) < (client.date_of_birth.month, client.date_of_birth.day))
        for client in clients
    ]

    avg_age = round(mean(client_ages), 2) if client_ages else 0
    med_age = round(median(client_ages), 2) if client_ages else 0

    ticket_type_counter = Counter(p.ticket.name for p in purchases)
    if ticket_type_counter:
        most_popular_ticket_type = ticket_type_counter.most_common(1)[0][0]
    else:
        most_popular_ticket_type = "Нет данных"

    profit_by_type = {}
    for p in purchases:
        key = p.ticket.name
        profit_by_type[key] = profit_by_type.get(key, 0) + p.ticket.price
    if profit_by_type:
        most_profitable_type = max(profit_by_type.items(), key=lambda x: x[1])[0]
    else:
        most_profitable_type = "Нет данных"

    return render(request, 'statistics.html', {
        'clients': clients,
        'total_sales': total_sales,
        'avg_sale': avg_sale,
        'med_sale': med_sale,
        'mode_sale': mode_sale,
        'avg_age': avg_age,
        'med_age': med_age,
        'most_popular_ticket_type': most_popular_ticket_type,
        'most_profitable_type': most_profitable_type,
    })
