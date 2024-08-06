# spamdetection/urls.py

from django.urls import path
from .views import UserRegistrationView, UserListCreateView, ContactListCreateView, SpamReportListCreateView, MarkNumberAsSpamView, SearchView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),
    path('spam-reports/', SpamReportListCreateView.as_view(), name='spam-report-list-create'),
    path('mark-spam/', MarkNumberAsSpamView.as_view(), name='mark-spam'),
    path('search/', SearchView.as_view(), name='search'),

]
