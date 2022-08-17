from django.shortcuts import render
from django.http import HttpResponse
from news.models import News, Category
from django.shortcuts import get_object_or_404, redirect
from news.forms import NewsForm
from django.views.generic import ListView

# Create your views here.


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    extra_context = {'title': 'Главная страница'}
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.exclude(is_published=0)
        return context

    # def get_queryset(self):
    #     return News.objects.exclude(is_published=True)


# def index(request):
#     news = News.objects.exclude(is_published=0)
#     context = {
#         'news': news,
#         'title': 'Новости'
#     }
#     return render(request, 'news/index.html', context)


class NewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.filter(category_id=self.kwargs['category_id'],
                                              is_published=1)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


# def get_category(request, category_id):
#     category = Category.objects.get(pk=category_id)
#     news = News.objects.filter(category_id=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, 'news/category.html', context)


def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    context = {
        'news_item': news_item
    }
    return render(request, 'news/view_news.html', context)


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            just_news = form.save()
            return redirect(just_news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
