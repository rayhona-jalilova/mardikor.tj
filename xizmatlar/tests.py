from django.test import TestCase

# Create your tests here.
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message.',
    'your-email@gmail.com',
    ['recipient-email@example.com'],
    fail_silently=False,
)
