from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from .models import User, Ticket
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm
from django.views.generic import TemplateView


class LoginView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                print('{} kullanıcısı tarafından başarılı giriş'.format(username))
                return redirect('/')
            else:
                messages.warning(request, 'Kullanıcı adınızı yada parolanızı yanlış girdiniz.')
        else:
            messages.warning(request, 'Kullanıcı adınızı yada parolanızı yanlış girdiniz.')
            return redirect('/login/')


class RegisterView(TemplateView):

    def get(self, request, *args, **kwargs):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return (HttpResponseRedirect('/'))
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        username = email = request.POST.get('email')
        post['username'] = email
        password = request.POST.get('password')
        profile_image = request.POST.get('profile_image')
        post['profile_image'] = profile_image
        request.POST = post
        form = UserRegisterForm(request.POST, files=request.FILES)
        if form.is_valid():  # and profile_form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, 'Welcome {}.Succesfully registered!You can login'.format(username))
            return (HttpResponseRedirect('/login/'))
        else:
            messages.warning(request, form.errors)
            return (HttpResponseRedirect('/register/'))


@login_required
def ulogout(request):
    logout(request)
    return (HttpResponseRedirect('/login/'))


def _403(request):
    return render(request, '403.html', {})


class TicketsView(TemplateView):
    template_name = 'ticket.track.html'

    def get(self, request, *args, **kwargs):
        extra_context = {
            'tickets': Ticket.objects.all(),
            'types': list(Ticket.type_options),
            'status': list(Ticket.status_options),
            'severity': list(Ticket.severity_options)
        }
        return render(request, 'ticket.track.html', extra_context)


class TicketView(TemplateView):
    template_name = 'ticket.track.html'

    def get(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'You have to login to look tickets!')
            return (HttpResponseRedirect('/login/'))
        context = super().get_context_data(**kwargs)
        ticket = get_object_or_404(Ticket, pk=pk)
        assignees = ticket.assignee.all()
        attachments = ticket.attachments.all()
        comments = ticket.comments.all()

        extra_context = {
            'ticket': ticket,
            'assignees': assignees,
            'attachments': attachments,
            'comments': comments
        }
        return render(request, 'ticket.view.html', extra_context)


class FilteredTicketView(TemplateView):
    template_name = 'ticket.track.html',

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'tickets': Ticket.label_search(Ticket, search=context['label']),
            'types': list(Ticket.type_options),
            'status': list(Ticket.status_options),
            'severity': list(Ticket.severity_options)
        }
        return render(request, self.template_name, extra_context)


class TeamsView(TemplateView):
    template_name = 'teams.html',

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {}
        return render(request, self.template_name, extra_context)


class UserProfileView(TemplateView):
    template_name = 'user.profile.html',

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = {
            'user': get_object_or_404(User, pk=context['pk']),
            'tickets': Ticket.get_user_tickets(Ticket, context['pk'])
        }
        return render(request, self.template_name, extra_context)


class OneTicketView(TemplateView):
    template_name = 'ticket.add.html',

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.warning(request, 'You have to login to look tickets!')
            return (HttpResponseRedirect('/login/'))

        context = super().get_context_data(**kwargs)

        extra_context = {
            'users': User.objects.all(),
            'types': list(Ticket.type_options),
            'status': list(Ticket.status_options),
            'severity': list(Ticket.severity_options)
        }
        return render(request, self.template_name, extra_context)
