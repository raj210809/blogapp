from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm, BlogForm
from .models import Blog
from django.urls import reverse
from django.http import JsonResponse

def index(request):
    blogs = Blog.objects.all()[:10]
    authenticated = request.user.is_authenticated
    return render(request, 'index.html', {'authenticated': authenticated,'blogs' : blogs})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def addblog(request , username):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.published_by = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'addblog.html', {'form': form})

def seeblog(request , blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request , 'seeblog.html',{'blog':blog})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile(request , username):
    blogs = Blog.objects.filter(published_by__username=username)
    user = username
    return render(request , 'profile.html' , {'blogs':blogs,'user':user})

def delete(request , blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect(reverse('profile', kwargs={'username': request.user.username}))

def suggestions(request):
    query = request.GET.get('query','')
    blogs = Blog.objects.filter(title__istartswith=query)[:5]
    suggestion = [blog.title for blog in blogs]
    return JsonResponse({'suggestion':suggestion})

def update(request, blog_id):
    if request.method == 'POST':
        blog = Blog.objects.get(id=blog_id)
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        blog = Blog.objects.get(id=blog_id)
        form = BlogForm(instance=blog)
    return render(request, 'update.html', {'form': form})