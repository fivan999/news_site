from django.shortcuts import render
from django.http import HttpResponse
from news.models import News, Category

# Create your views here.

def index(request):
    news = News.objects.exclude(is_published=0)
    context = {
        'news': news,
        'title': 'Новости',
        'category': 'Новости'
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
