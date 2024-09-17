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
        try:
            validate_password(value)
        except ValidationError as e:
            for msg in e.messages:
                if "too short" in msg:
                    raise serializers.ValidationError("PASSWORD_TOO_SHORT")
                elif "too common" in msg:
                    raise serializers.ValidationError("PASSWORD_TOO_COMMON")
                elif "entirely numeric" in msg:
                    raise serializers.ValidationError("PASSWORD_ONLY_NUMBERS")
                else:
                    raise serializers.ValidationError('UNKNOWN_ERROR')
            return value
