from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Users, Profiles
from .serializers import UserSerializer, ProfileSerializer

# Create your views here.
class GetAllUsers(APIView):
    def get(self, req):
        users = Users.objects.all()
        serialized_posts = UserSerializer(users, many=True) # 직렬화
        return Response(serialized_posts.data)

class CreateUser(APIView):
    def post(self, req):
        serializer = UserSerializer(data=req.data) # 역직렬화
        if serializer.is_valid():
            print("a: ", serializer)
            print("b: ", serializer.data)
            print("c: ", req)
            print("d: ", req.data)
            # user = serializer.save(commit=False)
            # user.writer = req.user
            # user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
