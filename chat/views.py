from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, loginSerializer, userSerializer, MessagesSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from chat.models import ChatModel
from hashlib import md5


# Create your views here.

class signUpUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        ser = SignupSerializer(data=request.data)
        
        if ser.is_valid():
            name = ser.validated_data['name']
            number = ser.validated_data['number']
            password = ser.validated_data['password']
            
            if User.objects.filter(username=number).exists():
                return Response({'message': 'User already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # user creation
            user = User.objects.create_user(
                username=number,  # phone number as the username
                password=password,
                first_name=name.split()[0],
                last_name = name.split()[1]
            )


            
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)



class loginUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        ser = loginSerializer(data=request.data)
        
        if ser.is_valid():
            username = ser.validated_data['number']
            password = ser.validated_data['password']
            
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    token,_ = Token.objects.get_or_create(user = user)
                    return Response({"Token": str(token)}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Wrong Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class getUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = User.objects.exclude(Q(username=request.user.username) | Q(username="admin"))
        ser = userSerializer(user, many = True)
        return Response(ser.data, status=status.HTTP_200_OK)


class getSelfInfo(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = User.objects.get(username=request.user.username)
        ser = userSerializer(user)
        return Response(ser.data, status=status.HTTP_200_OK)
    
class fetchOldMessages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_id = request.query_params.get('my_id')
        other_id = request.query_params.get('other_id')

        combined_ids = ''.join(sorted([str(my_id), str(other_id)]))
        room_name = md5(combined_ids.encode()).hexdigest()[:8]
        thread_name = f'chat_{room_name}'

        messages = ChatModel.objects.filter(thread_name = thread_name)
        ser = MessagesSerializer(messages,many = True)

        return Response(ser.data, status=status.HTTP_200_OK)