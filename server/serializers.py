from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    # Use Djangos built-in email validation
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=7)

    class Meta(object):
        model = User 
        fields = ['id', 'email', 'password']


    def validate_password(self, value):
        # Use Django's built-in password validators
        try:
            validate_password(value)
        except ValidationError as e:
            # Customize the error message here
            raise serializers.ValidationError({
                'password': ' '.join(e.messages)  # Combines all error messages into a single string
            })
        return value
