from django.utils import timezone
from rest_framework import status
from rest_framework import viewsets
from configurations.models import *
from configurations.serializers import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from configurations.token import get_access_token


class SignUpUserView(viewsets.ModelViewSet):

    def create(self,request):
        ''' Sign Up User '''
        serializer = SignUpUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"Created sucessfully and Otp sent successfully",
                        "success":True,
                         "data":serializer.data},
                         status=status.HTTP_201_CREATED)


class LogInUserView(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

    def create(self, request):
        ''' Add Address with lat long  '''
        data = request.data
        if 'mobile' and 'password' not in data:
        	return Response({"message": "please fill required fields email and password!"},
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(Account, mobile=data['mobile'])
        try:
            if user.check_password(data['password']):
                user.last_login = timezone.now()
                return Response({"token": get_access_token(user),
                                     "message": "SignUp successfully!"},
                                    status=status.HTTP_200_OK)
            return Response({"message": "Invalid credentials!"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Exception", e)
            return Response({"message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)



