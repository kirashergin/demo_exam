from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Post
import re



@login_required
def index_view(request):
    if request.method == "GET":
        if request.user.is_superuser:
            posts = Post.objects.all().order_by("timestamp")
        else:
            posts = Post.objects.filter(user=request.user)
        return render(request, "index.html", context={
            "posts": posts
        })
    
    
@login_required
def post_form_view(request):
    if request.method == "POST":
        plate = request.POST["plate"]
        description = request.POST["description"]

        try:
            post = Post.objects.create(plate=plate, description=description, user=request.user)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError as e:
            print(e)
            return render(request, "index.html", {
                "message": "Проверьте корректность введенных данных"
            })


def change_post_status_form_view(request):
    if not request.user.is_superuser or request.method != "POST":
        return render("index.html")
    
    post_id = request.POST["post_id"]
    status = request.POST["status"]

    post = Post.objects.get(pk=post_id)
    post.status = status
    post.save()
    return HttpResponseRedirect(reverse("index"))


def delete_post_form_view(request):
    if request.method != "POST":
        return render("index.html")
    
    post_id = request.POST["post_id"]
    post = Post.objects.get(pk=post_id)
    
    if post.user != request.user:
        return render("index.html")
    
    post.delete()
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Неверный логин или пароль."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]  
        password = request.POST["password"]
        name = request.POST["name"]
        phone = request.POST["phone"]

        if not username or not email or not password or not name or not phone:
            return render(request, "register.html", {
                "message": "Заполните все поля"
            })

        phone_pattern = re.compile(r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$')
        if not phone_pattern.match(phone):
            return render(request, "register.html", {
                "message": "Введите номер телефона в формате +7(XXX)-XXX-XX-XX"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password, name=name, phone=phone)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
