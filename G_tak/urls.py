from django.contrib import admin
from django.urls import path
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
        RestaurantCreateAPIView


from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
    





urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', APIHomeView.as_view(), name='home_api'),


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
]
