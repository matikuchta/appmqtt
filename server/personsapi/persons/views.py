from rest_framework import viewsets
from .models import Person, Job, UserRole
from .serializers import PersonSerializer, JobSerializer, UserSerializer, UserRoleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsAdminOrManager, IsManagerOrAdminForWrite, IsAdminOrCreateOnly, IsAuthenticatedForWrite
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseBadRequest
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from gmail_send import send_gmail
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string

# Job ViewSet
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()  # Query all Job objects
    serializer_class = JobSerializer  # Use JobSerializer to serialize data
    permission_classes = [IsManagerOrAdminForWrite]

# Person ViewSet
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()  # Query all Person objects
    serializer_class = PersonSerializer  # Use PersonSerializer to serialize data
    permission_classes = [IsAuthenticated]

class PersonByPeselView(APIView):
    def get(self, request, pesel, format=None):
        try:
            person = Person.objects.get(pesel=pesel)
            serializer = PersonSerializer(person)
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response({"detail": "Person not found."}, status=status.HTTP_404_NOT_FOUND)
    permission_classes = []
        


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrCreateOnly]



class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdminUser]


class ResetPasswordConfirmView(View):
    def get(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        if not uid or not token:
            return HttpResponseBadRequest("Missing uid or token.")
        return render(request, 'password_reset_confirm.html', {'uid': uid, 'token': token})

class GmailPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'

    def form_valid(self, form):
        # zamiast wysyłać przez send_mail(), wysyłamy przez Gmail API
        for user in self.get_users(form.cleaned_data["email"]):
            context = {
                'email': user.email,
                'domain': self.request.get_host(),
                'site_name': 'TwojaAplikacja',
                'uid': self.get_user_id(user),
                'user': user,
                'token': self.token_generator.make_token(user),
                'protocol': 'https' if self.request.is_secure() else 'http',
            }
            subject = render_to_string(self.subject_template_name, context).strip()
            body = render_to_string(self.email_template_name, context)

            send_gmail(subject, body, user.email) 

        return super().form_valid(form)

    def get_user_id(self, user):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        return urlsafe_base64_encode(force_bytes(user.pk))

