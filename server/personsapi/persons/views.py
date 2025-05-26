from rest_framework import viewsets
from .models import Person, Job, UserRole
from .serializers import PersonSerializer, JobSerializer, UserSerializer, UserRoleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsAdminOrManager, IsManagerOrAdminForWrite

# Job ViewSet
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()  # Query all Job objects
    serializer_class = JobSerializer  # Use JobSerializer to serialize data
    permission_classes = [IsManagerOrAdminForWrite]

# Person ViewSet
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()  # Query all Person objects
    serializer_class = PersonSerializer  # Use PersonSerializer to serialize data
    permission_classes = [IsManagerOrAdminForWrite]

class PersonByPeselView(APIView):
    def get(self, request, pesel, format=None):
        try:
            # Wyszukaj osobę po numerze pesel
            person = Person.objects.get(pesel=pesel)
            serializer = PersonSerializer(person)
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response({"detail": "Person not found."}, status=status.HTTP_404_NOT_FOUND)
    permission_classes = [IsManagerOrAdminForWrite]
        


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]



class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdminUser]

