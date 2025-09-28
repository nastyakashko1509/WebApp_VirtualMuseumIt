from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from museum_users.models import *
from museum_parts.models import *
from django.urls import reverse


def register_employee(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        position_id = request.POST.get('position')
        hall_ids = request.POST.getlist('halls')
        work_description = request.POST.get('work_description')
        photo = request.FILES.get('photo')
        date_of_birth = request.POST.get('date_of_birth')

        form_values = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'phone': phone,
            'bio': bio,
            'position': position_id,
            'work_description': work_description,
            'halls': hall_ids,
            'date_of_birth': date_of_birth,
        }

        if not (username and password and full_name):
            return render(request, 'register_employee.html', {
                'error': 'Обязательные поля не заполнены!',
                'positions': Position.objects.all(),
                'halls': Hall.objects.all(),
                'form_values': form_values,
                'selected_halls': hall_ids,
            })

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            error = "Пользователь с таким именем уже существует."
            return render(request, 'register_employee.html', {
                'error': error,
                'positions': Position.objects.all(),
                'halls': Hall.objects.all(),
                'form_values': form_values,
                'selected_halls': hall_ids,
            })

        photo_path = None
        if photo:
            fs = FileSystemStorage()
            photo_path = fs.save(f'photos/employees/{photo.name}', photo)

        employee = Employee(
            user=user,
            full_name=full_name,
            phone=phone,
            email=email,
            bio=bio,
            date_of_birth=date_of_birth,
            work_description=work_description,
            photo=photo_path,
            position_id=position_id
        )

        try:
            employee.full_clean()
            employee.save()
        except ValidationError as e:
            user.delete()
            return render(request, 'register_employee.html', {
                'error': e.message_dict,
                'positions': Position.objects.all(),
                'halls': Hall.objects.all(),
                'form_values': form_values,
                'selected_halls': hall_ids,
            })

        if hall_ids:
            employee.halls.set(hall_ids)

        return redirect('login')

    context = {
        'positions': Position.objects.all(),
        'halls': Hall.objects.all()
    }
    return render(request, 'register_employee.html', context)


def register_client(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('date_of_birth')
        phone = request.POST.get('phone')

        form_values = {
            'username': username,
            'email': email,
            'full_name': full_name,
            'date_of_birth': date_of_birth,
            'phone_number': phone
        }

        if not (username and password and full_name and date_of_birth):
            return render(request, 'register_client.html', {
                'error': 'Обязательные поля не заполнены!',
                'form_values': form_values,
            })

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            error = "Пользователь с таким именем уже существует."
            return render(request, 'register_client.html', {
                'error': error,
                'form_values': form_values,
            })

        client = Client(
            user=user,
            full_name=full_name,
            email=email,
            date_of_birth=date_of_birth,
            phone=phone
        )

        try:
            client.full_clean()
            client.save()
        except ValidationError as e:
            user.delete()
            return render(request, 'register_client.html', {
                'error': e.message_dict,
                'form_values': form_values,
            })

        return redirect('login')

    return render(request, 'register_client.html')


class RoleBasedLoginView(LoginView):

    def get_success_url(self):
        user = self.request.user
        
        if user.is_superuser:
            return reverse('admin_dashboard') 
        
        if hasattr(user, 'museum_employee'):
            return reverse('employee_dashboard') 
        
        if hasattr(user, 'museum_client'):
            return reverse('client_dashboard') 

        return reverse('main')
