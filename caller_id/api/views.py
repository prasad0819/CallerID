from .models import CustomUser

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from caller_id.api.serializers import CustomUserSerializer

class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    # Allow public access to `create` for user registration
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
