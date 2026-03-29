from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exam/<str:exam_name>/', views.exam_detail, name='exam_detail'),
    path('exam/<str:exam_name>/<str:year>/', views.papers_list, name='papers_list'),
]
