from django.urls import path
from . import views

app_name = 'editorial'

urlpatterns = [
    path('', views.index, name='index'),
    path('save/', views.save, name='save'),
    path('api/latest/', views.get_weekly_content, name='latest'),
]
