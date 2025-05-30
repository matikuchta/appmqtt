from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, JobViewSet, PersonByPeselView
from .views import UserViewSet, UserRoleViewSet, ResetPasswordConfirmView, GmailPasswordResetView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('password_reset_confirm/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/', GmailPasswordResetView.as_view(), name='password_reset'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
