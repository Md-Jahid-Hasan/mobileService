from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model as User


class UserDetailsSerializer(serializers.ModelSerializer):
    """Serializer for showing user Details"""
    isOwn = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User()
        fields = ['username', 'email', 'isOwn']

    def get_isOwn(self, obj):
        """Return if user have a active plan or not"""
        plan = obj.subscription.last()

        if plan.end_date:
            if timezone.now() <  plan.end_date:
                return True
        else:
            if plan.purchase_date + timedelta(30) > timezone.now():
                return True
        return False


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Return token for validate user with the user credential"""
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserDetailsSerializer(self.user).data

        for k, v in serializer.items():
            data[k] = v
        # data['username'] = self.user.name
        # data['email'] = self.user.email

        return data


class UserCreateSerializer(serializers.ModelSerializer, MyTokenObtainPairSerializer):
    """For creating user"""
    password1 = serializers.CharField(required=True, write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User()
        fields = ['username', 'email', 'password', 'password1', 'refresh', 'access']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password1'] != attrs['password']:
            raise serializers.ValidationError({'password': "Password Don't match"})
        return attrs

    def create(self, validated_data):
        """After create user also validate and return token"""
        validated_data.pop('password1')
        user = User().objects.create_user(**validated_data)
        validated_data.pop('username')

        data = MyTokenObtainPairSerializer.validate(self, validated_data)
        print(data)

        return data

class UserNumberUpdateSerializer(serializers.ModelSerializer):
    """Serializer for update/change user primary number"""
    class Meta:
        model = User()
        fields = ['primary_number']
