"""
URL configuration for caller_id project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from caller_id.api import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.CreateUserView.as_view(), name='register'),
    path('api/add-contact/', views.CreateContactView.as_view(), name='add-contact'),
    path('api/report-spam/', views.ReportSpamView.as_view(), name='report-spam'),
    path('api/search-by-name/', views.SearchContactByNameView.as_view(), name='search-by-name'),
    path('api/search-by-phone-number/', views.SearchContactByPhoneNumberView.as_view(), name='search-by-phone-number'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
