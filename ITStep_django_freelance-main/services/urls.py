from django.urls import path
from . import views

app_name = 'services'
urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('create/', views.service_create, name='service_create'),
    path('<int:pk>/update/', views.service_update, name='service_update'),
    path('<int:pk>/delete/', views.service_delete, name='service_delete'),
]
