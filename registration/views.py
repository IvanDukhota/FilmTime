from django.shortcuts import render
from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
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
                {"error": "Email не предоставлен"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Customer.objects.get(email=email)
            return Response(
                {"exists": True, "username": user.username}, status=status.HTTP_200_OK
            )
        except Customer.DoesNotExist:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)
