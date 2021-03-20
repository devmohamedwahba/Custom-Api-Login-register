from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer, CreateTokenSerializer, LogoutSerializer, VerifyTokenSerializer, TokenResetSerializer
from utils.renderers import UserRenderer
from .models import User, PhoneOtp
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from utils.email import Email
import jwt
from django.conf import settings
from utils.send_sms import otp_generator, TwilioSms


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    renderer_classes = (UserRenderer,)

    # @classmethod
    # def construct_link_to_verify_user(cls, request, user):
    #     token = RefreshToken.for_user(user).access_token
    #     current_site = get_current_site(request).domain
    #     relative_link = reverse('accounts:verify')
    #     abs_url = 'http://' + current_site + relative_link + '?token= ' + str(token)
    #     return abs_url

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(mobile=serializer.data.get('mobile', ''))
        otp = otp_generator()
        sms = TwilioSms(to=serializer.data.get('mobile', ''), body=otp)
        res = sms.send()
        if res:
            PhoneOtp.objects.create(otp=otp, user=user)

        # verified_url = RegisterView.construct_link_to_verify_user(request, user)
        # body = f""" Hi  Use This Link to Verify your email {verified_url}"""
        #
        # verified_email = Email(receiver='devmohamedwahba@gmail.com', sender='Mohamed Wahba',
        #                        subject='Verify User Account', body=body)
        # verified_email.send()

        return Response(data=serializer.data,
                        status=status.HTTP_201_CREATED)


class VerifyUserView(generics.GenericAPIView):
    serializer_class = VerifyTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(mobile=serializer.data.get('mobile'))
        if not user.is_verified:
            user.is_verified = True
            user.save()
        return Response(data={'data': 'User Activated Successful'}, status=status.HTTP_200_OK)

class TokenResetView(generics.GenericAPIView):
    serializer_class = TokenResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(mobile=serializer.data.get('mobile'))
        otp = otp_generator()
        sms = TwilioSms(to=serializer.data.get('mobile', ''), body=otp)
        res = sms.send()
        if res:
            PhoneOtp.objects.create(otp=otp, user=user)

        return Response(data={'data': 'Otp Sent Successful'}, status=status.HTTP_200_OK)




# class VerifyUserView(generics.GenericAPIView):
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY)
#             user = User.objects.get(id=payload['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response(data={'data': 'User Activated Successful'}, status=status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError:
#             return Response(data={'data': 'Link expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.InvalidTokenError:
#             return Response(data={'data': 'Token Invalid'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response(data={'data': 'Some thing happen too link'}, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(generics.GenericAPIView):
    serializer_class = CreateTokenSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)


class ManageUserView(generics.RetrieveUpdateAPIView):
    renderer_classes = (UserRenderer,)
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
