from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView

from main.forms import RegistrationForm


def get_menu_context():
    return [
        {'url_name': 'index', 'name': 'Главная'},
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
