from django.urls import path
from .views import genetic_test_list, genetic_test_create, genetic_test_delete, genetic_test_edit, statistics

urlpatterns = [
    path('', genetic_test_list, name='genetic_test_list'),
    path('create/', genetic_test_create, name='genetic_test_create'),
    path('delete/<int:pk>/', genetic_test_delete, name='genetic_test_delete'),
    path('edit/<int:pk>/', genetic_test_edit, name='genetic_test_edit'),
    path('statistics/', statistics, name='statistics'),
]