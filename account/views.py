from django.shortcuts import render,redirect
from rest_framework.views import APIView
from .srializers import UserRegistrationSerializers,User,UserLoginSerializer,UserRegistrarionModel
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import HttpResponse
from django.http import JsonResponse
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
        return redirect('https://668d5b1781675397e8330c4f--stellar-cheesecake-075991.netlify.app/login.html')
    else:
        return redirect('https://668d5b1781675397e8330c4f--stellar-cheesecake-075991.netlify.app/singup.html')


class UserLoginView(APIView):
    # serializer_class = UserLoginSerializer

    def post(self,request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request,username=username,password=password)
            print(user)

            getUser = login(request=request, user=user, backend='django.contrib.auth.backends.ModelBackend')
            print(getUser)

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

# class GetUserDetails(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request,pk):
#         try:
#             user = User.objects.get(pk=pk)
#             additional_info = UserRegistrarionModel.objects.get(user=user)
#         except(User.DoesNotExist):
#             return Http404
#         # serializer = UserRegistrationSerializers(user,additional_info)
#         context = {
#             'user_name':user.username,
#             'first_name':user.first_name,
#             'last_name':user.last_name,
#             'email':user.email,
#             'account_type':additional_info.account_type,
#             'image':additional_info.image,

#         }
#         serializer = UserRegistrarionModel(context)

#         return Response(serializer)
    
def GetUserDetails(request,pk):
    print("Get user details", pk)
    try:
        user = User.objects.get(id=pk)
        additional_info = UserRegistrarionModel.objects.get(user=pk)
        print(user,additional_info)
    except(User.DoesNotExist):
        user=None
        additional_info=None
        raise Http404
    
    # serializer = UserRegistrationSerializers(user,additional_info)
    context = {
            'user_name':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'account_type':additional_info.account_type,
            'image':str(additional_info.image),

        }
    # if serializer.is_valid():
    #     return Response(serializer.data)
    # raise Http404
    return JsonResponse(context)