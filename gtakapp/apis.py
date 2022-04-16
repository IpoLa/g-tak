from django.http import FileResponse
from rest_framework import filters
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
import django_filters.rest_framework

from gtakapp.models import Restaurant, \
    Meal, \
    Customer, \
    Driver, \
    Order, \
    OrderDetails, \
    Category

from gtakapp.serializers import MealSerializer, \
    MealDetailSerializer, \
    MealDetailUpdateSerializer, \
    CategorySerializer, \
    CategoryDetailSerializer, \
    CategoryDetailUpdateSerializer, \
    CustomerSerializer, \
    CustomerDetailSerializer, \
    CustomerDetailUpdateSerializer, \
    DriverSerializer, \
    DriverDetailSerializer, \
    DriverDetailUpdateSerializer, \
    RestaurantSerializer, \
    RestaurantDetailSerializer, \
    RestaurantDetailUpdateSerializer, \
    DriverSerializer, \
    DriverDetailSerializer, \
    DriverDetailUpdateSerializer



class APIHomeView(APIView):
    	# authentication_classes = [SessionAuthentication]
	# permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		data = {
			"auth": {
				"login_url":  api_reverse("auth_login_api", request=request),
				"refresh_url":  api_reverse("refresh_token_api", request=request), 
				# "user_checkout":  api_reverse("user_checkout_api", request=request), 
			},
			# "address": {
			# 	"url": api_reverse("user_address_list_api", request=request),
			# 	"create":   api_reverse("user_address_create_api", request=request),
			# },
			# "checkout": {
			# 	"cart": api_reverse("cart_api", request=request),
			# 	"checkout": api_reverse("checkout_api", request=request),
			# 	"finalize": api_reverse("checkout_finalize_api", request=request),
			# },
			"meals": {
				"count": Meal.objects.all().count(),
				"url": api_reverse("meals_api", request=request),
                "create": api_reverse("meals_create_api", request=request),
			},
			"categories": {
				"count": Category.objects.all().count(),
				"url": api_reverse("categories_api", request=request),
                "create": api_reverse("categories_create_api", request=request),
			},
			"restaurants": {
                "count": Restaurant.objects.all().count(),
				"url": api_reverse("restaurants_api", request=request),
                "create": api_reverse("restaurants_create_api", request=request),
			},
            "customers": {
				"count": Customer.objects.all().count(),
				"url": api_reverse("customers_api", request=request),
                "create": api_reverse("customers_create_api", request=request),
			},
            "drivers": {
				"count": Driver.objects.all().count(),
				"url": api_reverse("drivers_api", request=request),
                "create": api_reverse("drivers_create_api", request=request),
			},
		}
		return Response(data)



# Meal API
class MealListAPIView(generics.ListAPIView):  # Adding DocumentTokenMixin, DocumentUpdateAPIMixin, later
    	#permission_classes = [IsAuthenticated]
	queryset = Meal.objects.all()
	serializer_class = MealSerializer


class MealRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Meal.objects.all()
	serializer_class = MealDetailSerializer()


class MealCreateAPIView(generics.CreateAPIView):
	queryset = Meal.objects.all()
	serializer_class = MealDetailUpdateSerializer


# Category API
class CategoryListAPIView(generics.ListAPIView):  # Adding DocumentTokenMixin, DocumentUpdateAPIMixin, later
    	#permission_classes = [IsAuthenticated]
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Category.objects.all()
	serializer_class = CategoryDetailSerializer()


class CategoryCreateAPIView(generics.CreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategoryDetailUpdateSerializer



# Customer API
class CustomerRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer


class CustomerListAPIView(generics.ListAPIView):
    	#permission_classes = [IsAuthenticated]
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	search_fields = ["id", "phone"]


class CustomerCreateAPIView(generics.CreateAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerDetailUpdateSerializer



# # Driver API
class DriverRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverDetailSerializer


class DriverListAPIView(generics.ListAPIView):
    	#permission_classes = [IsAuthenticated]
	queryset = Driver.objects.all()
	serializer_class = DriverSerializer
	search_fields = ["id", "phone"]


class DriverCreateAPIView(generics.CreateAPIView):
	queryset = Driver.objects.all()
	serializer_class = DriverDetailUpdateSerializer



# # Restaurant API
class RestaurantRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer


class RestaurantListAPIView(generics.ListAPIView):
    	#permission_classes = [IsAuthenticated]
	queryset = Restaurant.objects.all()
	serializer_class = RestaurantSerializer
	search_fields = ["id", "phone"]


class RestaurantCreateAPIView(generics.CreateAPIView):
	queryset = Restaurant.objects.all()
	serializer_class = RestaurantDetailUpdateSerializer