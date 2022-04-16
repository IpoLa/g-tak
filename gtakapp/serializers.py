from rest_framework import serializers

from gtakapp.models import Restaurant, \
    Meal, \
    Customer, \
    Driver, \
    Order, \
    OrderDetails, \
    Category



# Convert each Restaurant and menu to JSON for REST API
class RestaurantSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, restaurant):
        request = self.context.get('request')
        logo_url = restaurant.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Restaurant
        fields = ("id", "name", "phone", "address", "logo")


# Convert each meal to JSON for REST API
class MealSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, meal):
        request = self.context.get('request')
        image_url = meal.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Meal
        fields = '__all__'




class MealDetailUpdateSerializer(serializers.ModelSerializer):
    # variation_set = VariationSerializer(many=True, read_only=True)
	# image = serializers.SerializerMethodField()
	class Meta:
		model = Meal
		fields = '__all__'

	def get_image(self, obj):
		try:
			return obj.image_set.first().image.url
		except:
			return None

	def create(self, validated_data):
		name = validated_data["name"]
		Meal.objects.get(name=name)
		meal = Meal.objects.create(**validated_data)
		return meal

	def update(self, instance, validated_data):
		instance.title = validated_data["name"]
		instance.save()
		return instance



class MealDetailSerializer(serializers.ModelSerializer):
    # variation_set = VariationSerializer(many=True, read_only=True)
	# product_image = serializers.SerializerMethodField()
	class Meta:
		model = Meal
		fields = '__all__'



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")


class CategoryDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='categories_detail_api')
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailUpdateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='categories_detail_api')
    class Meta:
        model = Category
        fields = [
            # "url",
            "id",
            "name",
        ]
    def create(self, validated_data):
        name = validated_data["name"]
        # Product.objects.get(title=title)
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        # instance.title = validated_data["title"]
        instance.save()
        return instance

class CustomerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='customers_detail_api')
    # variation_set = VariationSerializer(many=True)
    # product_image = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='customers_detail_api')
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerDetailUpdateSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='categories_detail_api')
    class Meta:
        model = Customer
        fields = '__all__'
    def create(self, validated_data):
        user = validated_data["user"]
        # Product.objects.get(title=title)
        customer = Customer.objects.create(**validated_data)
        return customer

    def update(self, instance, validated_data):
        # instance.title = validated_data["title"]
        instance.save()
        return instance




# Driver Serializer
class DriverSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='drivers_detail_api')
    # variation_set = VariationSerializer(many=True)
    # product_image = serializers.SerializerMethodField()
    class Meta:
        model = Driver
        fields = '__all__'

class DriverDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='drivers_detail_api')
    class Meta:
        model = Driver
        fields = '__all__'


class DriverDetailUpdateSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='categories_detail_api')
    class Meta:
        model = Driver
        fields = '__all__'
    def create(self, validated_data):
        user = validated_data["user"]
        # Product.objects.get(title=title)
        Driver = Driver.objects.create(**validated_data)
        return Driver

    def update(self, instance, validated_data):
        # instance.title = validated_data["title"]
        instance.save()
        return instance


    

# Restaurant Serializer
class RestaurantSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='restaurants_detail_api')
    # variation_set = VariationSerializer(many=True)
    # product_image = serializers.SerializerMethodField()
    class Meta:
        model = Restaurant
        fields = '__all__'

class RestaurantDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='restaurants_detail_api')
    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantDetailUpdateSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='categories_detail_api')
    class Meta:
        model = Restaurant
        fields = '__all__'
    def create(self, validated_data):
        user = validated_data["user"]
        # Product.objects.get(title=title)
        Restaurant = Restaurant.objects.create(**validated_data)
        return Restaurant

    def update(self, instance, validated_data):
        # instance.title = validated_data["title"]
        instance.save()
        return instance




# ORDER SERIALIZER
class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = '__all__'


class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = '__all__'


class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class OrderMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    meal = OrderMealSerializer()

    class Meta:
        model = OrderDetails
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    restaurant = OrderRestaurantSerializer()
    order_details = OrderDetailsSerializer(many=True)
    status = serializers.ReadOnlyField(source="get_status_display")

    class Meta:
        model = Order
        fields = '__all__'