from rest_framework import serializers
from .models import Person, Job, UserRole
from django.contrib.auth.models import User
import re

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'nazwa']
    def validate_nazwa(self, value):
        if (not re.search("^[A-Za-z]{1,}$", value)):
            raise serializers.ValidationError("job title must at least 2 characters long, and contain only letters")
        return value


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
        read_only_fields = ['data_utworzenia', 'data_modyfikacji']
    def validate_pesel(self, value):
        if (len(str(value))!=11):
            raise serializers.ValidationError("pesel must be 11 digit long")
        return value
    def validate_imie(self, value):
        if (not re.search("^[A-Za-z]{1}[a-z]{2,}$", value)):
            raise serializers.ValidationError("name must at least 3 characters long, contain only lowercase letters except the first character which can be uppercase")
        return value
    def validate_nazwisko(self, value):
        if (not re.search("^[A-Za-z]{1}[a-z]{1,}$", value)):
            raise serializers.ValidationError("surname must at least 2 characters long, contain only lowercase letters except the first character which can be uppercase")
        return value
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role']


