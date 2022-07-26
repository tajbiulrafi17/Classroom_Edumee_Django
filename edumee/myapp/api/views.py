
from itertools import permutations
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, StudentSignupSerializer, TeacherSignupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsStudentUser, IsTeacherUser


class TeacherSignupView(generics.GenericAPIView):
    serializer_class=TeacherSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message":"account created successfully"
        })

class StudentSignupView(generics.GenericAPIView):
    serializer_class=StudentSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message":"account created successfully"
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self,request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_teacher':user.is_teacher,
            'is_student':user.is_student
        })


class LogoutView(APIView):
    def post(self,request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class TeacherOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsTeacherUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user 


class StudentOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsStudentUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user 




