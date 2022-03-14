from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from main.forms import RegistrationForm, PizzaCreationForm
from main.models import Pizza


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
        {'url_name': 'assortment', 'name': 'Ассортимент'}
    ]


def index_page(request):
    context = {
        'pagename': 'Silver Pizza',
        'menu': get_menu_context()
    }
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
    context = {
        'menu': get_menu_context(),
        'user': get_object_or_404(User, username=username),
        'pagename': f'Профиль {username}'
    }
    return render(request, 'pages/profile/details.html', context)


def assortment(request):
    user = request.user
    context = {
        'pagename': 'Ассортимент',
        'menu': get_menu_context(),
        'user': user
    }
    pizzas = Pizza.get_all()
    context['pizzas'] = pizzas
    return render(request, 'pages/assortment.html', context)


def topsellers(request):
    context = {
        'pagename': 'Хиты продаж',
        'menu': get_menu_context()
    }
    pizzas = Pizza.objects.order_by('-rating')
    context['pizzas'] = pizzas
    return render(request, 'pages/topsellers.html', context)


def checkout(request):
    context = {
        'pagename': 'Корзина',
        'menu': get_menu_context()
    }
    return render(request, 'pages/checkout.html', context)


@staff_member_required
def adding_of_position(request):
    user = request.user
    context = {
        'pagename': 'Добавление позиции',
        'menu': get_menu_context(),
        'method': 'GET',
        'form': PizzaCreationForm()
    }
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
