from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("register", RegisterUser.as_view(), views.register),
    path("login", views.login),
    path("gallery", views.gallery),
    path("add", views.add),
    path("image/<str:url>", views.image),
    path("clear", views.clear),
]