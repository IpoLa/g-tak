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



from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import phoneModel
import base64





# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class getPhoneNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.counter += 1  # Update Counter At every Call
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(Mobile.counter))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.at(Mobile.counter)}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)


# Time after which OTP will expire
EXPIRY_TIME = 50 # seconds

class getPhoneNumberRegistered_TimeBased(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model for OTP is created
        print(OTP.now())
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.now()}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model 
        if OTP.verify(request.data["otp"]):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong/expired", status=400)







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
	serializer_class = CategoryDetailSerializer


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