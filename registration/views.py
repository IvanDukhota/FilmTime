from django.shortcuts import render
from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password

class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "id"

class CheckUserView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Customer.objects.get(email=email)
            return Response(
                {"exists": True, "username": user.username}, status=status.HTTP_200_OK
            )
        except Customer.DoesNotExist:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)

class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if Customer.objects.filter(email=email).exists():
            return Response(
                {
                    "error_code": 1001,
                    "error_message": "A user with this email already exists."
                },
                status=status.HTTP_409_CONFLICT
            )

        user = Customer.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()

        return Response({'message': 'User successfully registered!'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        users = Customer.objects.all()

        for user in users:
            if user.email == email and check_password(password, user.password):
                return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)

        return Response({'error': 'Incorrect email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
