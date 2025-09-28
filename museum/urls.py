from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from museum_authentication.views import *
from museum_information.views import *
from django.urls import path, include
from museum_graphics.views import *
from django.contrib import admin
from django.conf import settings
from museum_users.views import *
from museum_parts.views import *
from museum_base.views import *


urlpatterns = [
    # Страницы суперюзера (админа)
    path('admin/', admin.site.urls),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    
    # Главные страницы
    path('', home, name='home'),
    path('main/', main, name='main'),

    # Дополнительная страница (для выполнения всех заданий из ЛР)
    path('additional_page/', additional_page_view, name='additional_page'),

    # Страница с общедоступной информацией
    path('museum_info/', museum_info, name='museum_info'),

    # Аутентификация 
    path('login/', RoleBasedLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register-employee/', register_employee, name='register_employee'),
    path('register_client/', register_client, name='register_client'),

    # Страницы для перенаправления после входа
    path('employee/', employee_list, name='employee'),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),
    path('employee/(?P<employee_id>\d+)/', employee_detail, name='employee_detail'),
    path('client_dashboard/', client_dashboard, name='client_dashboard'),

    # Страницы с графиками и статистикой
    path('statistics/', statistics_view, name='statistics'),
    path('charts/age/', sales_by_visitor_age_chart, name='sales_by_age_chart'),
    path('charts/daytype/', sales_by_day_type_chart, name='sales_by_day_type_chart'),
    path('charts/overtime/', sales_over_time_chart, name='sales_over_time_chart'),
    path('charts/', sales_charts_page, name='sales_charts_page'),

    # Информационные страницы 
    path('news/', news_list, name='news_list'),
    path('about/', about_company_view, name='about'),
    path('privacy_policy/', privacy_policy_view, name='privacy_policy'),
    path('reviews/', reviews_view, name='reviews'),
    path('faq/', faq_list, name='faq_list'),
    path('promocodes/', promocodes_view, name='promocodes'),
    path('vacancies/', vacancies_view, name='vacancies'),
    path('joke/', programming_joke, name='joke'),

    # Страницы для управления товарами (билетами)
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),
    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:ticket_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('cart/checkout/', checkout_view, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
