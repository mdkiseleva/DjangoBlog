from django.shortcuts import redirect, render
from httpx import request
from .models import Article
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404
    
def logout_view(request):
    logout(request)
    return redirect('archive')
    
def create_post(request):
    if not request.user.is_authenticated:
        raise Http404

    if request.method == 'POST':
        form = {
            'title': request.POST.get('title', '').strip(),
            'text': request.POST.get('text', '').strip(),
        }

        if not form['title'] or not form['text']:
            form['errors'] = 'Не все поля заполнены'
            return render(request, 'create_post.html', {'form': form})

        if Article.objects.filter(title=form['title']).exists():
            form['errors'] = 'Статья с таким названием уже существует'
            return render(request, 'create_post.html', {'form': form})

        article = Article.objects.create(
            title=form['title'],
            text=form['text'],
            author=request.user
        )

        return redirect('get_article', article_id=article.id)

    return render(request, 'create_post.html', {'form': {}})

def register(request):
    if request.method == 'POST':
        form = {
            'username': request.POST.get('username', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'password': request.POST.get('password', '').strip(),
        }

        if not form['username'] or not form['email'] or not form['password']:
            form['errors'] = 'Не все поля заполнены'
            return render(request, 'register.html', {'form': form})

        if User.objects.filter(username=form['username']).exists():
            form['errors'] = 'Пользователь с таким именем уже существует'
            return render(request, 'register.html', {'form': form})

        User.objects.create_user(
            form['username'],
            form['email'],
            form['password']
        )

        return redirect('archive')

    return render(request, 'register.html', {'form': {}})

def login_view(request):
    if request.method == 'POST':
        form = {
            'username': request.POST.get('username', '').strip(),
            'password': request.POST.get('password', '').strip(),
        }

        if not form['username'] or not form['password']:
            form['errors'] = 'Не все поля заполнены'
            return render(request, 'login.html', {'form': form})

        user = authenticate(
            request,
            username=form['username'],
            password=form['password']
        )

        if user is None:
            form['errors'] = 'Нет аккаунта с таким сочетанием никнейма и пароля'
            return render(request, 'login.html', {'form': form})

        login(request, user)
        return redirect('archive')

    return render(request, 'login.html', {'form': {}})