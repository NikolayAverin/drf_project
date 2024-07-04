from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateApiView, PaymentListAPIView,
                         PaymentRetrieveApiView, UserCreateApiView,
                         UserDestroyApiView, UserListApiView,
                         UserRetrieveApiView, UserUpdateApiView)

app_name = UsersConfig.name

urlpatterns = [
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("register/", UserCreateApiView.as_view(), name="register"),
    path("list/", UserListApiView.as_view(), name="users"),
    path("<int:pk>/", UserRetrieveApiView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateApiView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDestroyApiView.as_view(), name="user_delete"),
    path("payments/create", PaymentCreateApiView.as_view(), name="payment_create"),
    path("payments/", PaymentListAPIView.as_view(), name="payments"),
    path(
        "payments/<int:pk>/", PaymentRetrieveApiView.as_view(), name="payments_detail"
    ),
]
