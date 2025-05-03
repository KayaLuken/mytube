from django.urls import path, include
from .views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('auth/', include((
        [
            path("register/", RegisterView.as_view(), name="register"),
            path("login/", TokenObtainPairView.as_view(), name="token_login"),
            path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        ],
        'auth'
    ))),
]