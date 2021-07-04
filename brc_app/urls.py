from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('users', views.users),
    path('user/add', views.user_add),
    path('user/edit/<int:user_id>', views.user_edit),
    path('user/delete/<int:user_id>', views.user_delete),
    path('employees', views.employees),
    path('employee/add', views.employee_add),
    path('employee/edit/<int:user_id>', views.employee_edit),
    path('employee/delete/<int:user_id>', views.employee_delete),
    path('customers', views.customers),
    path('customer/add', views.customer_add),
    path('customer/edit/<int:user_id>', views.customer_edit),
    path('customer/delete/<int:user_id>', views.customer_delete),
    path('trucking', views.trucking),
    path('trucking/add', views.trucking_add),
    path('trucking/edit/<int:user_id>', views.trucking_edit),
    path('trucking/delete/<int:user_id>', views.trucking_delete),
    path('customers', views.users),
    path('customer/add', views.user_add),
    path('customer/edit/<int:user_id>', views.user_edit),
    path('customer/delete/<int:user_id>', views.user_delete),
]
