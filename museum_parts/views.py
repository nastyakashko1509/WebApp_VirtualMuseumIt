from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from museum_users.models import ClientTicket
from django.views.generic import DetailView
from django.contrib import messages
from .models import *


# СТРАНИЦА "КАРТОЧКА ТОВАРА (БИЛЕТА)" 
# И УПРАВЛЕНИЕ ЕЮ (ДОБАВЛЕНИЕ В КОРЗИНУ, ПОКУПКА)

class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'ticket_detail.html'
    context_object_name = 'ticket'


@login_required
def cart_view(request):

    user_cart = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': user_cart})


@login_required
def add_to_cart(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)

    try:
        client = request.user.museum_client  
    except Client.DoesNotExist:
        return HttpResponseForbidden("Только клиенты могут покупать билеты.")

    Cart.objects.create(user=request.user, ticket=ticket)

    return redirect('cart_view')


@login_required
def remove_from_cart(request, cart_item_id):

    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    if request.method == 'POST':
        cart_item.delete()
    
    return redirect('cart_view')


@login_required
def update_cart_quantity(request, cart_item_id):

    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        elif action == 'decrease' and cart_item.quantity == 1:
            cart_item.delete()
    
    return redirect('cart_view')


@login_required
def checkout_view(request):
    
    user = request.user
    client = get_object_or_404(Client, user=user)
    cart_items = Cart.objects.filter(user=user)

    items_with_total = [
        {
            'ticket': item.ticket,
            'quantity': item.quantity,
            'total': item.ticket.price * item.quantity
        }
        for item in cart_items
    ]

    total_price = sum(item['total'] for item in items_with_total)

    if request.method == 'POST':
        if client.money >= total_price:
            client.money -= total_price
            client.save()

            for item in cart_items:
                ClientTicket.objects.create(
                    client=client,
                    ticket=item.ticket,
                    quantity=item.quantity
                )

            cart_items.delete()
            messages.success(request, f"Покупка успешно совершена! Потрачено {total_price}₽.")
            return redirect('cart_view')
        else:
            messages.error(request, "Недостаточно средств для оплаты.")

    return render(request, 'checkout.html', {
        'client': client,
        'cart_items': items_with_total,
        'total_price': total_price
    })
