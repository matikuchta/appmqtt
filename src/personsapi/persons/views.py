from rest_framework import viewsets
from .models import Person, Job
from .serializers import PersonSerializer, JobSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Job ViewSet
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()  # Query all Job objects
    serializer_class = JobSerializer  # Use JobSerializer to serialize data

# Person ViewSet
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()  # Query all Person objects
    serializer_class = PersonSerializer  # Use PersonSerializer to serialize data

class PersonByPeselView(APIView):
    def get(self, request, pesel, format=None):
        try:
            # Wyszukaj osobę po numerze pesel
            person = Person.objects.get(pesel=pesel)
            serializer = PersonSerializer(person)
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response({"detail": "Person not found."}, status=status.HTTP_404_NOT_FOUND)