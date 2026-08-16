from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),
             path('register/',views.register,name='register'),
             path('login/',views.user_login,name='user_login'),
             path('booking/',views.booking,name='booking'),
             path('user_logout/',views.user_logout,name='user_logout'),
            path('check-available/', views.check_available_rooms, name='check_available'),
            path('confirm/', views.confirm, name='confirm'),

             ]