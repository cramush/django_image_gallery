from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home),
    path("gallery", views.gallery),
    path("add", views.add),
    path("image/<str:url>", views.image),
    path("clear", views.clear),
]