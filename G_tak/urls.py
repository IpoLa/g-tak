from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token

from gtakapp.apis import APIHomeView, \
        MealListAPIView, \
        MealRetrieveAPIView, \
        MealCreateAPIView, \
        CategoryRetrieveAPIView, \
        CategoryCreateAPIView, \
        CategoryListAPIView, \
        CustomerRetrieveAPIView, \
        CustomerListAPIView, \
        CustomerCreateAPIView, \
        DriverRetrieveAPIView, \
        DriverListAPIView, \
        DriverCreateAPIView, \
        RestaurantRetrieveAPIView, \
        RestaurantListAPIView, \
        RestaurantCreateAPIView, \
        getPhoneNumberRegistered, \
        getPhoneNumberRegistered_TimeBased, \
        CustomerCreateOrderAPIView

from gtakapp import apis
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework.authtoken import views





urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', APIHomeView.as_view(), name='home_api'),

    path("verify/<phone>/", getPhoneNumberRegistered.as_view(), name="OTP Gen"),
    path("verify/time_based/<phone>/", getPhoneNumberRegistered_TimeBased.as_view(), name="OTP Gen Time Based"),

    path('api/auth/token/', obtain_jwt_token, name='auth_login_api'),
    path('api/auth/token/refresh/', refresh_jwt_token, name='refresh_token_api'),

    path('api/meals/', MealListAPIView.as_view(), name='meals_api'),
    path('api/meals/<int:pk>/', MealRetrieveAPIView.as_view(), name='meals_detail_api'),
    path('api/create-meal/', MealCreateAPIView.as_view(), name='meals_create_api'),

    path('api/categories/', CategoryListAPIView.as_view(), name='categories_api'),
    path('api/categories/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='categories_detail_api'),
    path('api/create-category/', CategoryCreateAPIView.as_view(), name='categories_create_api'),

    path('api/restaurants/', RestaurantListAPIView.as_view(), name='restaurants_api'),
    path('api/restaurants/<int:pk>/', RestaurantRetrieveAPIView.as_view(), name='restaurants_detail_api'),
    path('api/create-restaurant/', RestaurantCreateAPIView.as_view(), name='restaurants_create_api'),

    path('api/customers/', CustomerListAPIView.as_view(), name='customers_api'),
    path('api/customers/<int:pk>/', CustomerRetrieveAPIView.as_view(), name='customers_detail_api'),
    path('api/create-customer/', CustomerCreateAPIView.as_view(), name='customers_create_api'),

    path('api/drivers/', DriverListAPIView.as_view(), name='drivers_api'),
    path('api/drivers/<int:pk>/', DriverRetrieveAPIView.as_view(), name='drivers_detail_api'),
    path('api/create-driver/', DriverCreateAPIView.as_view(), name='drivers_create_api'),

    path('api/customer/order/create/', CustomerCreateOrderAPIView.as_view(), name='customers_order_create_api'),

    path('api/customer/order/add/', apis.customer_add_order),
    path('api/customer/order/latest/', apis.customer_get_latest_order),
    path('api/customer/driver/location/', apis.customer_driver_location),
    path('api/customer/order/history/', apis.customer_get_order_history),

    # APIs for DRIVERS
    path('api/driver/orders/ready/', apis.driver_get_ready_orders),
    path('api/driver/order/pick/', apis.driver_pick_order),
    path('api/driver/order/latest/', apis.driver_get_latest_order),
    path('api/driver/order/complete/', apis.driver_complete_order),
    path('api/driver/revenue/', apis.driver_get_revenue),
    path('api/driver/location/update/', apis.driver_update_location),
    path('api/driver/order/history/', apis.driver_get_order_history),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
