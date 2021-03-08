from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        user = self.request.data
        try:
            for field in ['email', 'password']:
                if not user.get(field):
                    return Response({f"{field} is required"}, status.HTTP_400_BAD_REQUEST)
            ALL_DATA_LIST = User.objects.all().values()
            USER_DATA_DICT = ALL_DATA_LIST[next((index for (index, d) in enumerate(ALL_DATA_LIST) if d["email"] == self.request.data['email']), None)]
            
            print("ALL_DATA_LIST = ", USER_DATA_DICT)
            _user = User.objects.get(email=self.request.data['email']) 

            if USER_DATA_DICT['password'] != self.request.data['password']:
                return Response({f"{field} Incorrect Password "}, status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken.for_user(_user)
            
            serializer = LoginSerializer(_user)
            _data = serializer.data
            _data.update({'token': str(token.access_token)})
            del _data['password']
            
            return Response({
                'status': True,
                'message': 'Login Successful',
                'data': _data
            })

        except Exception:
            return Response({f"{field} Doesn't Exists "}, status.HTTP_400_BAD_REQUEST)



class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        all_user = User.objects.all()
        global user_uuid
        global token
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user_uuid = user_data['uid']
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        relativeLink = "/auth/email-verify/"
        absurl = 'http://'+current_site+relativeLink+ user_uuid       
        email_body = 'Hi '+ "User" + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'} 
        send_mail('Verify your email' ,email_body, 'rbprimevideo@gmail.com',[user.email],)
        return Response(user_data, status = status.HTTP_201_CREATED)
       
class VerifyEmail(generics.GenericAPIView):
    def get(self, request, pk):
        
        try:
            payload = jwt.decode(jwt=str(token), key=settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id = payload['user_id'])
            if not user.is_active and user_uuid == pk:
                user.is_active = True
                user.save()
                return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            else:
                return Response({'email': 'UUID is Wrong'}, status.HTTP_400_BAD_REQUEST)

        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
