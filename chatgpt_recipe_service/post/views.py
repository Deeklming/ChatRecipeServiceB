from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

# Create your views here.
# class RestIndex(APIView):
#     def get(self, req):
#         posts = Post.objects.all()
#         serialized_posts = PostSerializer(posts, many=True) # 직렬화
#         return Response(serialized_posts.data)

# class RestWrite(APIView):
#     def post(self, req):
#         serializer = PostSerializer(data=req.data) # 역직렬화
#         if serializer.is_valid():
#             post = serializer.save(commit=False)
#             post.writer = req.user
#             post.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
