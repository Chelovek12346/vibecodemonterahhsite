from django.urls import path
from . import views

app_name = "funding"

urlpatterns = [
    path('summary/', views.funding_summary),
    path('donate/', views.donate),
]

