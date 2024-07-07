from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .srializers import UserRegistrationSerializers,User,UserLoginSerializer
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# Create your views here.

class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializers

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user[0])
            uid = urlsafe_base64_encode(force_bytes(user[0].pk))

            email_subject = 'Confirm your email.'
            confirm_link = f'https://online-school-lr66.onrender.com/account/active/{uid}/{token}/'
            email_body=render_to_string('./account/confirm_email.html',{'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to=[user[0].email])
            email.attach_alternative(email_body,'text/html')
            email.send()

            return Response('Done')
        return Response('Sorry')
    

def ActiveAccount(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    print(user)
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('registration')
    else:
        return redirect('registration')


class UserLoginView(APIView):
    # serializer_class = UserLoginSerializer

    def post(self,request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username,password=password)

            login(request=request, user=user, backend='django.contrib.auth.backends.ModelBackend')

            if user:
                token,_ = Token.objects.get_or_create(user=user)
                return Response({'token':str(token),'user_id':user.id})
            else:
                return Response({"error":"Invalid credentials"})
        else:
            return Response(serializer.errors)
        
class LogoutView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')