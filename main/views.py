from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
import json

from main.forms import RegistrationForm, PizzaCreationForm, CheckoutForm
from main.models import Pizza, Order, OrderItem, OrderData
from main.utils import cookieCart


def get_base_context(request, pagename):
    context = {
        'menu': get_menu_context(),
        'pagename': pagename,
    }
    return context


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'assortment', 'name': 'Ассортимент'}
    ]


def index_page(request):
    context = get_base_context(request, 'Silver Pizza')
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        notifications = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        notifications = cookieData['notifications']
        order = cookieData['order']
        items = cookieData['items']
    context['notifications'] = notifications
    context['items'] = items
    context['order'] = order
    return render(request, 'pages/index.html', context)


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = get_menu_context()
        context['pagename'] = 'Регистрация'
        return context


@login_required
def profile_details_page(request, username):
    context = get_base_context(request, f'Профиль {username}')
    context['points'] = request.user.customer.bonus_points
    context['user'] = get_object_or_404(User, username=username)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    notifications = order.get_cart_items
    context['order'] = order
    context['notifications'] = notifications
    return render(request, 'pages/profile/details.html', context)


def assortment(request):
    user = request.user
    context = get_base_context(request, 'Ассортимент')
    context['user'] = user
    pizzas = Pizza.get_all()
    active_filter = ''
    if request.method == 'POST':
        selected = request.POST.getlist('list_of_types')
        if selected == ['chicken']:
            pizzas = Pizza.get_all().filter(type=0)
            active_filter = 'с курицей'
        if selected == ['beef']:
            pizzas = Pizza.get_all().filter(type=1)
            active_filter = 'с говядиной'
        if selected == ['sausage']:
            pizzas = Pizza.get_all().filter(type=2)
            active_filter = 'с колбасой'
        if selected == ['vegetarian']:
            pizzas = Pizza.get_all().filter(type=3)
            active_filter = 'вегетарианская'
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        notifications = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        notifications = cookieData['notifications']
        order = cookieData['order']
        items = cookieData['items']
    context['notifications'] = notifications
    context['items'] = items
    context['order'] = order
    context['pizzas'] = pizzas
    context['active_filter'] = active_filter
    return render(request, 'pages/assortment.html', context)


def topsellers(request):
    context = get_base_context(request, 'Хиты продаж')
    pizzas = Pizza.objects.order_by('-rating')

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        notifications = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        notifications = cookieData['notifications']
        order = cookieData['order']
        items = cookieData['items']
    context['notifications'] = notifications
    context['pizzas'] = pizzas
    context['items'] = items
    context['order'] = order
    return render(request, 'pages/topsellers.html', context)


def checkout(request):
    context = get_base_context(request, 'Корзина')
    context['method'] = 'GET'
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        context['notifications'] = order.get_cart_items
        items = order.orderitem_set.all()
        context['form'] = CheckoutForm()
        if request.method == 'POST':
            address = OrderData()
            address.save()
            form = CheckoutForm(request.POST, request.FILES, instance=address)
            if form.is_valid():
                form.save()
                order = Order.objects.create()
                customer.bonus_points += order.get_bonus_points
                customer.save()
                return redirect("/payment/")
    else:
        context['form'] = CheckoutForm()
        if request.method == 'POST':
            address = OrderData()
            address.save()
            form = CheckoutForm(request.POST, request.FILES, instance=address)
            if form.is_valid():
                form.save()
                return redirect("/payment/")
        cookieData = cookieCart(request)
        notifications = cookieData['notifications']
        order = cookieData['order']
        items = cookieData['items']
        context['notifications'] = notifications
    context['items'] = items
    context['order'] = order
    return render(request, 'pages/checkout.html', context)


@staff_member_required
def adding_of_position(request):
    context = get_base_context(request, 'Добавление позиции')
    user = request.user
    context['method'] = 'GET'
    context['form'] = PizzaCreationForm()
    if request.method == 'POST':
        pizza = Pizza(
            author=user,
            price=0,
            rating=0
        )
        pizza.save()
        form = PizzaCreationForm(request.POST, request.FILES, instance=pizza)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/assortment/')
        context['form'] = form
    return render(request, 'pages/creating_position.html', context)


def update_item(request):
    data = json.loads(request.body)
    pizzaId = data['pizzaId']
    action = data['action']

    customer = request.user.customer
    pizza = Pizza.objects.get(id=pizzaId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, pizza=pizza)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    print('Action:', action)
    print('pizzaId:', pizzaId)
    return JsonResponse('Item Was Added', safe=False)


def payment(request):
    context = get_base_context(request, 'Оплата')
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        notifications = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        notifications = cookieData['notifications']
        order = cookieData['order']
        items = cookieData['items']
    context['notifications'] = notifications
    context['items'] = items
    context['order'] = order
    return render(request, 'pages/payment.html', context)
