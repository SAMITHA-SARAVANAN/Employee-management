from django.urls import path
from . import views


urlpatterns = [
    path('', views.employee_login, name='employee_login'),
    path('admin-login', views.login_view, name='login'),    
    path('index/', views.index, name='index'),
    path('user-dashboard/', views.employee_details, name='user_dashboard'),  
    path('submit-request/', views.submit_request, name='submit_request'),
    path('admin-dashboard/', views.dashboard_with_notifications, name='admin_dashboard'),
    path('clear-notifications/', views.clear_notifications, name='clear_notifications'),
    
    #path('', views.index, name="index"),
    path('view_info/<int:id>/', views.view_info, name='view_info'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('update/<int:id>/', views.update_employee, name='update_employee'), 
    path('logout/', views.logout_view, name='logout'),   

]

