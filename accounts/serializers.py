from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.text import gettext_lazy as _
from .models import PhoneOtp

from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('mobile', 'password', 'name', 'is_staff')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # def validate(self, attrs):
    #     mobile = attrs.get('mobile', '')
    #     if mobile:
    #         pass
    #     return attrs

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class TokenResetSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, validators=[RegexValidator(regex='^01[0|1|2|5][0-9]{8}$',
                                                                             message="Phone number must be : 010 or 011 or 012 or 015.",
                                                                             code="Invalid Phone Number")])


class VerifyTokenSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, validators=[RegexValidator(regex='^01[0|1|2|5][0-9]{8}$',
                                                                             message="Phone number must be : 010 or 011 or 012 or 015.",
                                                                             code="Invalid Phone Number")])
    token = serializers.CharField(max_length=4)

    def validate(self, attrs):
        mobile = attrs.get("mobile", '')
        token = attrs.get("token", '')
        otp = PhoneOtp.objects.filter(user__mobile=mobile, otp=token).first()
        if not otp:
            raise AuthenticationFailed('Otp Validation Error')
        return attrs


class CreateTokenSerializer(serializers.Serializer):
    mobile = serializers.CharField(write_only=True)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True
    )
    tokens = serializers.CharField(read_only=True, max_length=255)

    def validate(self, attrs):
        mobile = attrs.get("mobile")
        password = attrs.get("password")
        user = authenticate(mobile=mobile, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credentials')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled please contact admin')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled please contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Account is Not Verified')

        # attrs['user'] = user
        return {
            "tokens": user.tokens()
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
