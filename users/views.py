from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import *
from .permissions import Is_Student
from users.models import Account, Student
from users.serializers import AccountSerializer, StudentSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=AccountSerializer
    )
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # JWT token yaratish
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'success': True,
                    'message': "Account created successfully!",
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': user.username,
                    'role': user.role
                },
                status=HTTP_201_CREATED
            )
        return Response(
            {
                'success': False,
                'errors': serializer.errors
            },
            status=HTTP_400_BAD_REQUEST
        )


class AccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AccountSerializer

    @swagger_auto_schema(
        request_body=AccountSerializer
    )
    def get_object(self):
        return self.request.user


class StudentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [Is_Student]

    serializer_class = StudentSerializer

    @swagger_auto_schema(
        request_body=StudentSerializer
    )
    def get_object(self):
        return Student.objects.get(user=self.request.user)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not old_password or not new_password or not confirm_password:
            return Response({'errors': "Barcha maydonlarni to'liq kiriting!"}, status=HTTP_400_BAD_REQUEST)

        if not check_password(old_password, user.password):
            return Response({'errors': "Eski parol noto'g'ri!"}, status=HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'errors': "Yangi parol mos emas!"}, status=HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response(
            {
                'success': True,
                'message': "Parol changed successfully!",
            },
            status=HTTP_200_OK
        )
