from statistics import mean, median, mode, StatisticsError
from django.contrib.auth.decorators import login_required
from museum_users.models import Client, Position
from django.shortcuts import render, redirect
from django.shortcuts import render
from datetime import date
from .models import *
import requests


@login_required
def news_list(request):
    
    all_news = News.objects.order_by('-published_at')
    
    news_list = []
    for news in all_news:
        news_list.append({
            'id': news.id,
            'title': news.title,
            'short_description': news.short_description,
            'first_sentence': news.get_first_sentence(),
            'full_content': news.content,
            'image': news.image,
            'published_at': news.published_at
        })
    
    return render(request, 'news_list.html', {'all_news': news_list})


@login_required
def about_company_view(request):

    about = AboutCompany.objects.first()
    return render(request, 'about_company.html', {'about': about})


@login_required
def privacy_policy_view(request):    
    return render(request, 'privacy_policy.html')


@login_required
def reviews_view(request):

    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        try:
            Review.objects.create(author=request.user, text=text, rating=int(rating))
        except Exception as e: ...
        return redirect('reviews')

    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': reviews})


@login_required
def faq_list(request):

    if request.method == 'POST':
        question_text = request.POST.get('question', '').strip()
        if question_text:
            try:
                FAQ.objects.create(question=question_text)
            except Exception as e: ...
            return redirect('faq_list')

    faqs = FAQ.objects.order_by('-added_date')
    return render(request, 'faq_list.html', {'faqs': faqs})


@login_required
def promocodes_view(request):

    today = date.today()
    active_codes = PromoCode.objects.filter(is_active=True, valid_until__gte=today).order_by('valid_until')
    archived_codes = PromoCode.objects.filter(is_active=False) | PromoCode.objects.filter(valid_until__lt=today)
    archived_codes = archived_codes.distinct().order_by('-valid_until')

    return render(request, 'promocodes.html', {
        'active_codes': active_codes,
        'archived_codes': archived_codes,
    })


@login_required
def vacancies_view(request):

    positions = Position.objects.all()
    return render(request, 'vacancies.html', {'positions': positions})


@login_required
def programming_joke(request):

    joke_url = "https://official-joke-api.appspot.com/jokes/programming/random"
    giphy_api_key = "55RXs3hObNGRt48Ava5HmkZSS992vBtI"
    giphy_url = "https://api.giphy.com/v1/gifs/random"

    try:
        response = requests.get(joke_url)
        response.raise_for_status()
        joke = response.json()[0]
    except Exception:
        joke = {"setup": "Ошибка загрузки шутки.", "punchline": ""}

    gif_url = None
    try:
        params = {
            "api_key": giphy_api_key,
            "tag": "programming",
            "rating": "g"
        }
        gif_response = requests.get(giphy_url, params=params)
        gif_response.raise_for_status()
        gif_data = gif_response.json()
        gif_url = gif_data.get("data", {}).get("images", {}).get("downsized_medium", {}).get("url")
    except Exception:
        gif_url = None  

    return render(request, "joke.html", {"joke": joke, "gif_url": gif_url})
