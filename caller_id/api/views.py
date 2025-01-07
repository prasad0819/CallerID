from .models import CustomUser, Contact, SpamReport

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from caller_id.api.serializers import ContactSerializer, CustomUserSerializer, SpamReportSerializer

class CreateUserView(CreateAPIView):
    model = CustomUser
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        self.create_contact(instance)

    def create_contact(self, user):
        contact = Contact.objects.create(
            full_name=user.full_name,
            phone_number=user.phone_number,
            owner=user
        )
        contact.save()

class CreateContactView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ReportSpamView(CreateAPIView):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)
