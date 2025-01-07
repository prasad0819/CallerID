from .models import CustomUser, Contact, SpamReport

from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from caller_id.api.serializers import ContactSerializer, CustomUserSerializer, SpamReportSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import models

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


class SearchContactByNameView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        full_name = request.query_params.get('full_name', None)
        if full_name is None:
            return Response(
                {"error": "full_name is a required query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        contacts = Contact.objects.filter(full_name__istartswith=full_name).order_by('full_name')
        contacts_contains = Contact.objects.filter(full_name__icontains=full_name).order_by('full_name')
        contacts = contacts | contacts_contains

        spam_reports = SpamReport.objects.values('phone_number').annotate(count=models.Count('phone_number'))

        spam_report_dict = {}
        for spam_report in spam_reports:
            spam_report_dict[spam_report['phone_number']] = spam_report['count']

        response = []
        for contact in contacts:
            response.append({
                "full_name": contact.full_name,
                "phone_number": str(contact.phone_number),
                "spam_report_count": spam_report_dict.get(str(contact.phone_number), 0)
            })

        return Response(response, status=status.HTTP_200_OK)


class SearchContactByPhoneNumberView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        phone_number = request.query_params.get('phone_number', None)
        if phone_number is None:
            return Response(
                {"error": "phone_number is a required query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        custom_user = CustomUser.objects.filter(phone_number=phone_number).first()
        contacts = Contact.objects.filter(phone_number=phone_number)

        spam_reports = SpamReport.objects.values('phone_number').annotate(count=models.Count('phone_number'))

        spam_report_dict = {}
        for spam_report in spam_reports:
            spam_report_dict[spam_report['phone_number']] = spam_report['count']

        response = []
        if custom_user is not None:
            current_user_as_contact = Contact.objects.filter(owner=custom_user, phone_number=request.user.phone_number).first()
            response.append({
                "full_name": custom_user.full_name,
                "phone_number": str(custom_user.phone_number),
                "email": custom_user.email if current_user_as_contact else "",
                "spam_report_count": spam_report_dict.get(str(custom_user.phone_number), 0)
            })

            return Response(response, status=status.HTTP_200_OK)
        
        for contact in contacts:
            response.append({
                "full_name": contact.full_name,
                "phone_number": str(contact.phone_number),
                "spam_report_count": spam_report_dict.get(str(contact.phone_number), 0)
            })

        return Response(response, status=status.HTTP_200_OK)