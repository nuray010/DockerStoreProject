from .models import (UserProfile, Category, SubCategory, Product, ProductImage, Review,Cart,CartItem, Favorite,FavoriteItem)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username', 'password', 'email', 'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }






class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']




class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_image', 'category_name']


class SubCategoryListSerializer(serializers.ModelSerializer):
        class Meta:
            model = SubCategory
            fields = ['id', 'subcategory_name']



class SubCategoryNameSerializer(serializers.ModelSerializer):
        class Meta:
            model = SubCategory
            fields = [ 'subcategory_name']




class CategoryDetailSerializer(serializers.ModelSerializer):
    sub_categories = SubCategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'sub_categories']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductListSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    created_date = serializers.DateField(format='%d-%m-%Y')
    subcategory = SubCategoryListSerializer()
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','price', 'product_name', 'product_type',
                  'product_images', 'created_date', 'subcategory',
                  'get_avg_rating', 'get_count_people']

    def get_get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_get_count_people(self, obj):
        return obj.get_count_people()




class SubCategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
            model = SubCategory
            fields = ['subcategory_name', 'products']



class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format('%d-%m-%Y'))
    user = UserProfileSimpleSerializer()
    class Meta:
        model = Review
        fields = ['user', 'stars', 'comment' ,'created_date']


class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    created_date = serializers.DateField(format='%d-%m-%Y')
    subcategory = SubCategoryListSerializer()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['product_name', 'subcategory', 'price', 'product_images', 'video',
                  'article_number', 'description', 'product_type', 'created_date', 'reviews']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    get_total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'get_total_price']

    def get_get_total_price(self, obj):
        return obj.get_total_price()





class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'



class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'








