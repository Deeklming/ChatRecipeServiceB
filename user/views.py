from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserAllSerializer

# Create your views here.
class UserAll(APIView):
    def post(self, req):
        try:
            serialized_user = UserAllSerializer(req.user)
            return Response(serialized_user.data, 200)
        except Exception as e:
            return Response({'UserAll error' : e}, 403)
