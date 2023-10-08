from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostAllSerializer, CommentAllSerializer

# Create your views here.
class PostAll(APIView):
    def post(self, req):
        try:
            serialized_body = PostAllSerializer(req.body)
            return Response(serialized_body.data, 200)
        except Exception as e:
            return Response({'PostAll error' : e}, 403)

class CommentAll(APIView):
    def post(self, req):
        try:
            serialized_body = CommentAllSerializer(req.body)
            return Response(serialized_body.data, 200)
        except Exception as e:
            return Response({'CommentAll error' : e}, 403)
