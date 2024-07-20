from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Course, Enrollment, PasswordChangeRequest, RegisterAttempt, EmailChangeRequest, GroupChat, HelpRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(username=user.username, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid email or password")

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class PasswordChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordChangeRequest
        fields = '__all__'

class RegisterAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterAttempt
        fields = '__all__'

class EmailChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailChangeRequest
        fields = '__all__'

class GroupChatSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupChat
        fields = '__all__'

class HelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = '__all__'
