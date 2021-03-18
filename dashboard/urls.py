from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    # post views
    #path('login/', views.user_login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('lastUpdated', views.lastUpdated),
    path('publish', views.publish),

]
