from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("post_form", views.post_form_view, name="post_form"),
    path("change_post_status_form", views.change_post_status_form_view, name="change_post_status_form"),
    path("delete_post_form", views.delete_post_form_view, name="delete_post_form"),
]