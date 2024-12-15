from django.urls import path
from web_scraping_app import views

urlpatterns = [
    path('', views.index, name="index"),
]
