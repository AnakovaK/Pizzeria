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
from main.utils import cookieCart, cart_data


def get_base_context(pagename):
    """
    Функция базового контекста для страницы

    :param menu: Меню вверху страницы
    :param pagename: Название страницы
    :return: Возвращает базовый контекст страницы.
    """
    context = {
        'menu': get_menu_context(),
        'pagename': pagename,
    }
    return context


def get_menu_context():
    """
    Функция меню в верхней части на всех страницах.

    :return: Возвращает меню вверху.
    """
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'assortment', 'name': 'Ассортимент'}
    ]


def index_page(request):
    """
    Функция главной страницы.

    :param notifications: Количество уведомлений в корзине
    :return: Возвращает страницу с наименованием "Silver Pizza" и количеством товара в корзине.
    """
    context = get_base_context('Silver Pizza')
    data = cart_data(request)
    context['notifications'] = data['notifications']
    return render(request, 'pages/index.html', context)


class RegistrationView(CreateView):
    """
    Функция страницы регистрации пользователя.

    :param menu: Всё меню вверху страницы
    :param pagename: Название страницы
    :param form_class: Заранее заданная форма из forms.py для регистрации нового пользователя
    :return: Возвращает страницу с формой регистрации для пользователя.
    """
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
    """
    Функция профиля пользователя.

    :param points: Количество бонусных очков пользователя
    :param customer: Пользователь
    :param notifications: Количество товаров, добавленных в корзину
    :return: Возвращает страницу профиля пользователя.
    """
    context = get_base_context(f'Профиль {username}')
    context['points'] = request.user.customer.bonus_points
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    context['notifications'] = order.get_cart_items
    return render(request, 'pages/profile/details.html', context)


def assortment(request):
    """
    Функция страницы с ассортиментом товаров.

    :param pizzas: Вся пицца из базы данных (или отфильтрованная по заданному параметру)
    :param active_filter: Активированный пользователем фильтр для пиццы
    :param notifications: Количество уведомлений в корзине
    :return: Возвращает страницу с ассортиментом пиццы из базы данных и возможностью ее фильтровать по начинке.
    """
    context = get_base_context('Ассортимент')
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
    data = cart_data(request)
    context['notifications'] = data['notifications']
    context['pizzas'] = pizzas
    context['active_filter'] = active_filter
    return render(request, 'pages/assortment.html', context)


def topsellers(request):
    """
    Функция страницы с хитами продаж.

    :param notifications: Количество уведомлений в корзине
    :param data: Все данные о заказе на данный момент
    :param pizzas: Вся отфильтрованная по пуполярности пицца на данный момент
    :return: Возвращает страницу с наименованием "Хиты продаж" и отсортированной по популярности пиццы.
    """
    context = get_base_context('Хиты продаж')
    data = cart_data(request)
    context['notifications'] = data['notifications']
    context['pizzas'] = Pizza.objects.order_by('-rating')
    return render(request, 'pages/topsellers.html', context)


def checkout(request):
    """
    Функция страницы с оплатой Paypal.

    :param method: Метод обращения к странице (Изначально GET, после нажатия на клавишу "добавить" - POST)
    :param order: Заказ пользователя на данный момент
    :param items: Все товары, добавленные в заказ
    :param address: Адрес и телефон заказчика
    :param form: Заранее заданная форма из forms.py для оформления заказа
    :return: Возвращает страницу со страницей корзины
    """
    context = get_base_context('Корзина')
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
        order = cookieData['order']
        items = cookieData['items']
        context['notifications'] = cookieData['notifications']
    context['items'] = items
    context['order'] = order
    return render(request, 'pages/checkout.html', context)


@staff_member_required
def adding_of_position(request):
    """
    Функция страницы с оплатой Paypal.

    :param method: Метод обращения к странице (Изначально GET, после нажатия на клавишу "добавить" - POST)
    :param form: Заранее заданная форма из forms.py для создания новой позиции пиццы
    :param pizza: Модель одной пиццы для заполнения формы
    :return: Возвращает страницу, которая предназначена для добавления нового вида пиццы в ассортимент товаров.
    """
    context = get_base_context('Добавление позиции')
    context['method'] = 'GET'
    context['form'] = PizzaCreationForm()
    if request.method == 'POST':
        pizza = Pizza(
            author=request.user,
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
    """
     Функция изменения товара.

     :param pizzaId: ID пиццы
     :param pizza: Пицца по Id
     :param action: Действие, производимое над товаром (увеличение или уменьшение количества товара)
     :param customer: Пользователь
     :return: Возвращает JSON о том, что предмет был изменен
     """
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
    return JsonResponse('Item Was Added', safe=False)


def payment(request):
    """
    Функция страницы с оплатой Paypal.

    :param notifications: Количество уведомлений в корзине
    :param data: Все данные о заказе на данный момент
    :return: Возвращает страницу с наименованием "оплата" и количеством товара в корзине
    """
    context = get_base_context('Оплата')
    data = cart_data(request)
    context['notifications'] = data['notifications']
    return render(request, 'pages/payment.html', context)
