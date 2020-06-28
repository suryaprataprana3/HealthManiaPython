from configurations.views import *
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'sessions', SignUpUserView)
urlpatterns = router.urls

urlpatterns += [

    path('v1/sign-up/', SignUpUserView.as_view({'post': 'create'})),
    path('v1/log-in/', LogInUserView.as_view({'post': 'create'})),


]
