from django.urls import path
from . import views

# ex: /polls/5/
#path('<int:question_id>/', views.detail, name='detail'),
app_name = "emptyseat"
urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form, name='form'),
    path('setup_schedule/', views.setup_schedule, name='setup_schedule')
]