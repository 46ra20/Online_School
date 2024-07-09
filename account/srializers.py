from rest_framework import serializers
from .models import UserRegistrarionModel
from django.contrib.auth.models import User

ACCOUNT_TYPE = [
    ('STUDENT','Student'),
    ('TEACHER','Teacher'),
]

class UserRegistrationSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()
    account_type = serializers.ChoiceField(choices=ACCOUNT_TYPE)
    confirm_password=serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password','account_type','image']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        account_type = self.validated_data['account_type']
        image = self.validated_data['image']

        if password!=confirm_password:
            raise serializers.ValidationError({'error':"password didn't match"})
        # if password != '/^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$/':
        #     raise serializers.ValidationError({'error':'Please enter a strong password'})
        
        if User.objects.filter(email=email):
            raise serializers.ValidationError({'error':"Email alrady exist"})

        account = User(username=username,first_name=first_name,last_name=last_name,email=email)
        user_model = UserRegistrarionModel(user=account,account_type=account_type,image=image)
        
        if account_type=='TEACHER':
            account.is_staff=True

        account.set_password(password)
        account.is_active=False
        account.save()
        user_model.save()

        return account,user_model
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User