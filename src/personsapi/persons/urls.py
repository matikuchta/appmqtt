from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, JobViewSet, PersonByPeselView

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('', include(router.urls)), 
    path('person/pesel/<int:pesel>/', PersonByPeselView.as_view(), name='person-by-pesel'),
]
