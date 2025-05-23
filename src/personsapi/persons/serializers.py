from rest_framework import serializers
from .models import Person, Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'nazwa']


# Serializer dla osoby (Person)
class PersonSerializer(serializers.ModelSerializer):
    stanowisko = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())  # Używamy ID stanowiska

    class Meta:
        model = Person
        fields = [
            'id', 'imie', 'nazwisko', 'pesel', 'stanowisko', 
            'data_urodzenia', 'data_zatrudnienia', 
            'data_modyfikacji', 'data_utworzenia'
        ]
