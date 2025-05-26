from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, JobViewSet, PersonByPeselView
from .views import UserViewSet, UserRoleViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'users', UserViewSet)
router.register(r'user-roles', UserRoleViewSet)
urlpatterns = [
    path('', include(router.urls)), 
    path('person/pesel/<int:pesel>/', PersonByPeselView.as_view(), name='person-by-pesel'),
      path('api-auth/', include('rest_framework.urls')),
]
