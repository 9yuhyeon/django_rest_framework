from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
# Create your views here.

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class FollowView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        me = request.user
        if me in user.follower.all():
            user.follower.remove(me)
            return Response({"msg":"팔로우 취소!"}, status=status.HTTP_200_OK)
        else:
            user.follower.add(me)
            return Response({"msg":"팔로우!"}, status=status.HTTP_200_OK)