from django.shortcuts import render
from django.http import HttpResponse
from news.models import News, Category
from django.shortcuts import get_object_or_404, redirect
from news.forms import NewsForm
from django.core.files.storage import FileSystemStorage

# Create your views here.


def index(request):
    news = News.objects.exclude(is_published=0)
    context = {
        'news': news,
        'title': 'Новости'
    }
    return render(request, 'news/index.html', context)


def get_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    news = News.objects.filter(category_id=category_id)
    context = {
        'news': news,
        'category': category
    }
    return render(request, 'news/category.html', context)


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
