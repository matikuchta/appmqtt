from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

class Person(models.Model):
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    pesel = models.IntegerField(unique=True)
    stanowisko = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="stanowisko")
    data_urodzenia = models.DateField()
    data_zatrudnienia = models.DateField()
    data_modyfikacji = models.DateTimeField(auto_now=True)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

class UserRole(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

