# spamdetection/views.py

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import User, Contact, SpamReport
from .serializers import UserSerializer, ContactSerializer, SpamReportSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

class SpamReportListCreateView(generics.ListCreateAPIView):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]

class MarkNumberAsSpamView(generics.CreateAPIView):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        reporter = request.user
        phone_number = data.get('phone_number')

        # Check if the number is already marked as spam by the reporter
        if SpamReport.objects.filter(reporter=reporter, phone_number=phone_number).exists():
            return Response({'detail': 'Number already marked as spam by the user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the number as spam
        serializer = self.get_serializer(data={'reporter': reporter.id, 'phone_number': phone_number})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Number marked as spam successfully.'}, status=status.HTTP_201_CREATED)

class SearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', '')

        # Search by name
        name_results = User.objects.filter(username__icontains=query)
        phone_results = User.objects.filter(phone_number=query)

        # Combine and order results
        results = list(name_results) + list(phone_results)
        return results
