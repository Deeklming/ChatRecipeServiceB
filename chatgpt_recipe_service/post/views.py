from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from .permissions import NewReadOnly


# @api_view(['GET'])
class PostsList(APIView):
    def get(self, req):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     permission_classes = [NewReadOnly]
#     # filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['user', 'likes']

#     def get_serializer_class(self):
#         if self.action == 'list' or 'retrieve':
#             return PostSerializer
#         return PostCreateSerializer

#     # def perform_create(self, serializer):
#     #     profile = Profile.objects.get(user=self.req.user)
#     #     serializer.save(author=self.req.user, profile=profile)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def like_post(req, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if req.user in post.likes.all():
#         post.likes.remove(req.user)
#     else:
#         post.likes.add(req.user)

#     return Response({'status': 'ok'})
