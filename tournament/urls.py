from django.urls import path

import views

urlpatterns = [
    path('register', views.RegisterAPIView.as_view(), name='register')
]
