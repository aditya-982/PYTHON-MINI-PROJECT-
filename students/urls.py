from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_student, name='search_student'),
    path('analytics/', views.student_analytics, name='student_analytics'),
]