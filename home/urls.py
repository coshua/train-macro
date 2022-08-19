from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.init, name='init'),
    path('state/', views.state, name='state')
]