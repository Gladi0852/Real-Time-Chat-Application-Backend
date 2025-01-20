from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from chat.models import ChatModel

# Define a phone number validator for 10-digit numbers
phone_number_validator = RegexValidator(
    regex=r'^\d{10}$',  # Ensures only 10 digits are allowed
    message="Phone number must be 10 digits."
)

class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    number = serializers.CharField(
        max_length=10,  # Ensure the length is exactly 10 characters
        validators=[phone_number_validator]  # Apply the phone number validator
    )
    password = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'}, 
        min_length=8
    )  # User's password with min length and password field styling


class loginSerializer(serializers.Serializer):
    number = serializers.CharField(
        max_length=10, 
        validators=[phone_number_validator]
    )
    password = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'}, 
        min_length=8
    )

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']
        extra_kwargs = {'username':{'read_only':True}}

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ['username','message']