
from django.urls import path
from mainapp import views

urlpatterns = [
    path('', views.home,name='home'),
    path('employee/<int:employee_id>/update/', views.update_employee, name='update_employee'),
    path('employee/<int:employee_id>/delete/', views.delete_employee, name='delete_employee'),
]
