from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("add", views.add),
    path("image/<str:url>", views.image),
    path("clear", views.clear),
]