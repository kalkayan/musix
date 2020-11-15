import django.shortcuts as S
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return S.render(request, 'pages/dashboard.html')


def welcome(request):
    return S.render(request, 'pages/welcome.html')
