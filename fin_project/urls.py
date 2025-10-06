"""
URL configuration for the fin_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from fin_project.apps.bookings.views import BookingListCreateView, BookingCancelView, BookingDecisionView
from fin_project.apps.reviews.views import ReviewCreateView, ReviewRetrieveUpdateDestroyView, ReviewListView
from fin_project.apps.listings.views import (PropertyListCreateView, PropertyRetrieveUpdateDestroyView,
                                             PropertyToggleStatusView)
from fin_project.apps.users.views import RegisterView, LoginView, LogoutView
from fin_project.apps.search.views import PopularListingsView,  PopularSearchesView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
     path('register/', RegisterView.as_view(), name='register'),
     path('login/', LoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

     path('properties/', PropertyListCreateView.as_view(), name='property-list-create'),
     path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view(), name='property-detail'),
     path('properties/<int:pk>/toggle-status/', PropertyToggleStatusView.as_view(), name='property-toggle-status'),

     path('bookings/', BookingListCreateView.as_view(), name='booking_list'),
     path('bookings/<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel-renter'),        #renter
     path('bookings/<int:pk>/decision/', BookingDecisionView.as_view(), name='booking-decision-landlord'),  # owner

     path('reviews/', ReviewListView.as_view(), name='review_list'),
     path('reviews/booking/<int:booking_id>/', ReviewCreateView.as_view(), name='review-create'),
     path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),

     path("popular-searches/", PopularSearchesView.as_view(), name="popular-searches"),
     path("popular-listings/", PopularListingsView.as_view(), name="popular-listings"),
      ])),       ]

schema_view = get_schema_view(
    openapi.Info(
        title="Task API",
        default_version="v1",
        description="API Documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns +=   [
     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_docs'),
     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_docs')
                 ]
# path('token/blacklist/', TokenBlacklistView.as_view(), name='token-blacklist'),№



