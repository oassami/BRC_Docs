from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('users', views.users),
    path('user/add', views.user_add),
    path('user/edit/<int:user_id>', views.user_edit),
    path('user/delete/<int:user_id>', views.user_delete),
    path('employee', views.employees),
    path('employee/add', views.employee_add),
    path('employee/edit/<int:emp_id>', views.employee_edit),
    path('employee/inactive/<int:emp_id>', views.employee_inactive),
    path('customer', views.others),
    path('customer/add', views.other_add),
    path('customer/edit/<int:other_id>', views.other_edit),
    path('customer/inactive/<int:other_id>', views.other_inactive),
    path('supplier', views.others),
    path('supplier/add', views.other_add),
    path('supplier/edit/<int:other_id>', views.other_edit),
    path('supplier/inactive/<int:other_id>', views.other_inactive),
    path('trucking', views.others),
    path('trucking/add', views.other_add),
    path('trucking/edit/<int:other_id>', views.other_edit),
    path('trucking/inactive/<int:other_id>', views.other_inactive),

    path('receiving', views.receiving),
    path('receiving/add', views.receiving_add),
    path('production', views.production),
    path('production/add', views.production_add),
]
