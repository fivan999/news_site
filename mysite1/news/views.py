from django.db.models import Q
from django.shortcuts import render
import urllib
from django.http import HttpResponse
from news.models import News, Category
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from news.forms import NewsForm, UserRegisterForm, UserLoginForm, MailSendForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.core.paginator import Paginator
from django.conf import settings
import json


def get_captcha_result(req):
    recaptcha_response = req.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result


# def create_mailing(request):
#     if request.method == 'POST':
#         form = MailSendForm(request.POST)
#         if form.is_valid():
#             result = get_captcha_result(request)
#             if result['success']:
#                 subject = form.cleaned_data['subject']
#                 text = form.cleaned_data['text']
#                 receivers_list = form.cleaned_data['receivers'].split(' ')
#                 result = send_mail(
#                     subject, text, 'ivan.filato2007@gmail.com',
#                     receivers_list, fail_silently=True
#                 )
#                 if result:
#                     messages.success(request, 'Отправка успешна')
#                 else:
#                     messages.error(request, 'Ошибка отправки')
#                 return redirect('send_mail')
#             else:
#                 messages.error(request, 'Invalid reCAPTCHA')
#                 return redirect('send_mail')
#         else:
#             messages.error(request, 'Форма заполнена неверно')
#     else:
#         form = MailSendForm()
#     return render(request, 'news/send-mail.html', {'form': form})


class MailView(FormView):
    form_class = MailSendForm
    template_name = 'news/send-mail.html'

    def form_valid(self, form):
        if form.is_valid():
            result = get_captcha_result(self.request)
            if result['success']:
                subject = form.cleaned_data['subject']
                text = form.cleaned_data['text']
                receivers_list = form.cleaned_data['receivers'].split(' ')
                result = send_mail(
                    subject, text, 'ivan.filato2007@gmail.com',
                    receivers_list, fail_silently=True
                )
                if result:
                    messages.success(self.request, 'Отправка успешна')
                else:
                    messages.error(self.request, 'Ошибка отправки')
                return redirect('send_mail')
            else:
                messages.error(self.request, 'Invalid reCAPTCHA')
                return redirect('send_mail')
        else:
            messages.error(self.request, 'Форма заполнена неверно')
            return redirect('send_mail')


def user_logout(request):
    logout(request)
    return redirect('home')


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             messages.success(request, 'Регистрация успешна')
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Ошибка регистрации')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'news/register.html', {'form': form})


class RegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'news/register.html'

    def form_valid(self, form):
        if form.is_valid():
            result = get_captcha_result(self.request)
            if result['success']:
                user = form.save()
                messages.success(self.request, 'Регистрация успешна')
                login(self.request, user)
                return redirect('home')
            else:
                messages.error(self.request, 'Invalid reCAPTCHA')
                return redirect('register')
        else:
            messages.error(self.request, 'Ошибка регистрации')
            return redirect('register')


# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, 'Успешный вход')
#             return redirect('home')
#     else:
#         form = UserLoginForm()
#     return render(request, 'news/login.html', {'form': form})


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'news/login.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.get_user()
            login(self.request, user)
            messages.success(self.request, 'Успешный вход')
            return redirect('home')
        else:
            messages.error(self.request, 'Неверные данные')


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    extra_context = {'title': 'Главная страница'}
    allow_empty = True
    paginate_by = 2

    def get_queryset(self):
        search_query = self.request.GET.get('search_req', None)
        if search_query is not None:
            return News.objects.exclude(is_published=0).filter(Q(title__icontains=search_query) | Q(content__icontains=search_query)).select_related('category')
        return News.objects.exclude(is_published=0).select_related('category')


# def index(request):
#     news = News.objects.exclude(is_published=0)
#     context = {
#         'news': news,
#         'title': 'Новости'
#     }
#     return render(request, 'news/index.html', context)


class NewsByCategory(ListView):
    paginate_by = 2
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=1).select_related('category')


# def get_category(request, category_id):
#     category = Category.objects.get(pk=category_id)
#     news = News.objects.filter(category_id=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, 'news/category.html', context)


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'item'


# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item
#     }
#     return render(request, 'news/view_news.html', context)


class CreateNews(LoginRequiredMixin, CreateView):
    template_name = 'news/add_news.html'
    form_class = NewsForm
    login_url = '/login/'
    # success_url = reverse_lazy('home')

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             just_news = form.save()
#             return redirect(just_news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
