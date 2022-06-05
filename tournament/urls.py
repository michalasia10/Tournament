from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tournament import views

router = DefaultRouter()
router.register('register', views.RegisterAPIView, basename='RegisterAPIView')

urlpatterns = [
    path('v1/', include([
        path('', include(router.urls))
    ]))
]

urlpatterns += [
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
