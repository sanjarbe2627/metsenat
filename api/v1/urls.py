from django.urls import path, include
from rest_framework_simplejwt import views

from api.v1.sponsor import urls as sponsor_urls
from api.v1.student import urls as student_urls

urlpatterns = [
    path('auth/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/refresh/blacklist', views.TokenBlacklistView.as_view(), name='token_blacklist'),

    path('sponsor/', include(sponsor_urls)),
    path('student/', include(student_urls)),
]
