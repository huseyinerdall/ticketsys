from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views
from app.views import FilteredTicketView, TicketView, RegisterView, TicketsView, LoginView, \
    TeamsView, UserProfileView
from django.conf import settings
from django.conf.urls.static import static
from .models import User, Ticket

app_name = 'app'

urlpatterns = [
                  path('ticket/view/<int:pk>', TicketView.as_view()),
                  path('', TicketsView.as_view()),
                  path('/tickets', TicketsView.as_view()),
                  path('ticket/add/', TemplateView.as_view(template_name='ticket.add.html',
                                                           extra_context={'users': User.objects.all(),
                                                                          'types': list(Ticket.type_options),
                                                                          'status': list(Ticket.status_options)}),
                       name='add_ticket'),
                  path('search/<str:label>', FilteredTicketView.as_view()),
                  path('login/', LoginView.as_view(), name='ulogin'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('teams/', TeamsView.as_view()),
                  path('user/profile/<int:pk>', UserProfileView.as_view()),
                  path('logout', views.ulogout, name='ulogout'),
                  path('403', views._403, name='403'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
