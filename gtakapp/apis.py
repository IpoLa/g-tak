from django.http import FileResponse
from rest_framework import filters
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
import django_filters.rest_framework


import json
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.models import AccessToken

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
    DriverDetailUpdateSerializer, \
    OrderSerializer

from rest_framework.authtoken.models import Token



from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import phoneModel
import base64

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


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





@csrf_exempt
def customer_add_order(request):
    """
        params:
            access_token
            restaurant_id
            address
            order_details (json format), example:
                [{"meal_id": 1, "quantity": 2},{"meal_id": 2, "quantity": 3}]
            stripe_token
        return:
            {"status": "success"}
    """

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(
            token=request.POST.get("access_token"), expires__gt=timezone.now())

        # Get profile
        customer = access_token.user.customer

        # Get Stripe token
        stripe_token = request.POST["stripe_token"]

        # Check whether customer has any order that is not delivered
        if Order.objects.filter(customer=customer).exclude(
                status=Order.DELIVERED):
            return Response({
                "status": "failed",
                "error": "Your last order must be completed."
            })

        # Check Address
        if not request.POST["address"]:
            return Response({
                "status": "failed",
                "error": "Address is required."
            })

        # Get Order Details
        order_details = json.loads(request.POST["order_details"])

        order_total = 0
        for meal in order_details:
            order_total += Meal.objects.get(
                id=meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:

            # Step 1: Create a charge: this will charge customer's card
            charge = stripe.Charge.create(
                amount=order_total * 100,  # Amount in cents
                currency="usd",
                source=stripe_token,
                description="FoodTasker Order")

            if charge.status != "failed":
                # Step 2 - Create an Order
                order = Order.objects.create(
                    customer=customer,
                    restaurant_id=request.POST["restaurant_id"],
                    total=order_total,
                    status=Order.COOKING,
                    address=request.POST["address"])

                # Step 3 - Create Order details
                for meal in order_details:
                    OrderDetails.objects.create(
                        order=order,
                        meal_id=meal["meal_id"],
                        quantity=meal["quantity"],
                        sub_total=Meal.objects.get(id=meal["meal_id"]).price *
                        meal["quantity"])

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({
                    "status": "failed",
                    "error": "Failed connect to Stripe."
                })


def customer_get_latest_order(request):
    access_token = AccessToken.objects.get(
        token=request.GET.get("access_token"), expires__gt=timezone.now())

    customer = access_token.user.customer
    order = OrderSerializer(
        Order.objects.filter(customer=customer).last()).data

    return JsonResponse({"order": order})


def customer_driver_location(request):
    access_token = AccessToken.objects.get(
        token=request.GET.get("access_token"), expires__gt=timezone.now())

    customer = access_token.user.customer

    # Get driver's location related to this customer's current order.
    current_order = Order.objects.filter(customer=customer,
                                         status=Order.ONTHEWAY).last()
    location = current_order.driver.location

    return JsonResponse({"location": location})


# GET params: access_token
def customer_get_order_history(request):
    access_token = AccessToken.objects.get(
        token=request.GET.get("access_token"), expires__gt=timezone.now())
    customer = access_token.user.customer

    order_history = OrderSerializer(Order.objects.filter(
        customer=customer, status=Order.DELIVERED).order_by("picked_at"),
                                    many=True,
                                    context={
                                        "request": request
                                    }).data

    return JsonResponse({"order_history": order_history})


####################################################
# RESTAURANTS
####################################################
# get a list of order notifications made AFTER last_request_time for restaurant
def restaurant_order_notification(request, last_request_time):
    notification = Order.objects.filter(
        restaurant=request.user.restaurant,
        created_at__gt=last_request_time).count()

    return JsonResponse({"notification": notification})


####################################################
# DRIVERS
####################################################
def driver_get_ready_orders(request):
    orders = OrderSerializer(Order.objects.filter(status=Order.READY,
                                                  driver=None).order_by("-id"),
                             many=True).data

    return JsonResponse({"orders": orders})


@csrf_exempt
# POST
# params: access_token, order_id
def driver_pick_order(request):

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(
            token=request.POST.get("access_token"), expires__gt=timezone.now())

        # Get Driver
        driver = access_token.user.driver

        # Check if driver can only pick up one order at the same time
        if Order.objects.filter(driver=driver).exclude(status=Order.DELIVERED):
            return JsonResponse({
                "status":
                "failed",
                "error":
                "You can only pick one order at the same time."
            })

        try:
            order = Order.objects.get(id=request.POST["order_id"],
                                      driver=None,
                                      status=Order.READY)
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        except Order.DoesNotExist:
            return JsonResponse({
                "status":
                "failed",
                "error":
                "This order has been picked up by another."
            })

    return JsonResponse({})


# GET params: access_token
def driver_get_latest_order(request):
    # Get token
    access_token = AccessToken.objects.get(
        token=request.GET.get("access_token"), expires__gt=timezone.now())

    driver = access_token.user.driver
    order = OrderSerializer(
        Order.objects.filter(driver=driver).order_by("picked_at").last()).data

    return JsonResponse({"order": order})


# POST params: access_token, order_id
@csrf_exempt
def driver_complete_order(request):
    # Get token
    access_token = AccessToken.objects.get(
        token=request.POST.get("access_token"), expires__gt=timezone.now())

    driver = access_token.user.driver

    order = Order.objects.get(id=request.POST["order_id"], driver=driver)
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})


# GET params: access_token
def driver_get_revenue(request):
    access_token = AccessToken.objects.get(
        token=request.GET.get("access_token"), expires__gt=timezone.now())

    driver = access_token.user.driver

    from datetime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [
        today + timedelta(days=i)
        for i in range(0 - today.weekday(), 7 - today.weekday())
    ]

    for day in current_weekdays:
        orders = Order.objects.filter(driver=driver,
                                      status=Order.DELIVERED,
                                      created_at__year=day.year,
                                      created_at__month=day.month,
                                      created_at__day=day.day)

        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})


# POST - params: access_token, "lat,lng"
@csrf_exempt
def driver_update_location(request):
    if request.method == "POST":
        access_token = AccessToken.objects.get(
            token=request.POST.get("access_token"), expires__gt=timezone.now())

        driver = access_token.user.driver

        # Set location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "Driver location successfully sent"})


# GET params: access_token
def driver_get_order_history(request):
    access_token = AccessToken.objects.get(
        token=request.GET.get("access_token"), expires__gt=timezone.now())
    driver = access_token.user.driver

    order_history = OrderSerializer(Order.objects.filter(
        driver=driver, status=Order.DELIVERED).order_by("picked_at"),
                                    many=True,
                                    context={
                                        "request": request
                                    }).data

    return JsonResponse({"order_history": order_history})