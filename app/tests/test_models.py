from django.test import TestCase
from unittest.mock import patch
from app.mail_service import SendinBlue_Mail_Service

from app.models import SkyAthlete, UltraAthlete

class UltraAthleteTestCase(TestCase):
    def setUp(self):
        self.ultra_athlete_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'email': 'john@example.com',
            'gender': 'Male',
            'first_link': 'https://www.example.com/first',
            'second_link': 'https://www.example.com/second',
        }

    def test_ultra_athlete_creation(self):
        athlete = UltraAthlete.objects.create(**self.ultra_athlete_data)
        self.assertEqual(athlete.first_name, 'John')
        self.assertEqual(athlete.last_name, 'Doe')
        self.assertEqual(athlete.phone, '1234567890')
        self.assertEqual(athlete.email, 'john@example.com')
        self.assertEqual(athlete.gender, 'Male')
        self.assertFalse(athlete.paid)
        self.assertIsNone(athlete.payment_mail)
        self.assertEqual(athlete.first_link, 'https://www.example.com/first')
        self.assertEqual(athlete.second_link, 'https://www.example.com/second')

    @patch.object(SendinBlue_Mail_Service, 'send_email')
    def test_send_mail(self, mock_send_email):
        athlete = UltraAthlete.objects.create(**self.ultra_athlete_data)

        mock_send_email.return_value = 'mail_sent'
        result = athlete.send_mail()

        self.assertEqual(result, 'mail_sent')
        mock_send_email.assert_called_with(
            {"email": "balkanultra.noreply@gmail.com", "name": "Balkan Ultra"},
            [{"email": athlete.email, "name": athlete.first_name}],
            "78",
            [{"email": "balkanultra@abv.bg", "name": "Rosen Rusev"}]
        )

    def test_ultra_athlete_str(self):
        athlete = UltraAthlete.objects.create(**self.ultra_athlete_data)
        self.assertEqual(str(athlete), 'John Doe')


class SkyAthleteTestCase(TestCase):
    def setUp(self):
        self.sky_athlete_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone': '0987654321',
            'email': 'jane@example.com',
            'gender': 'Female',
        }

    def test_sky_athlete_creation(self):
        athlete = SkyAthlete.objects.create(**self.sky_athlete_data)
        self.assertEqual(athlete.first_name, 'Jane')
        self.assertEqual(athlete.last_name, 'Doe')
        self.assertEqual(athlete.phone, '0987654321')
        self.assertEqual(athlete.email, 'jane@example.com')
        self.assertEqual(athlete.gender, 'Female')
        self.assertFalse(athlete.paid)
        self.assertIsNone(athlete.payment_mail)

    @patch.object(SendinBlue_Mail_Service, 'send_email')
    def test_send_mail(self, mock_send_email):
        athlete = SkyAthlete.objects.create(**self.sky_athlete_data)

        mock_send_email.return_value = 'mail_sent'
        result = athlete.send_mail()

        self.assertEqual(result, 'mail_sent')
        mock_send_email.assert_called_with(
            {"email": "balkanultra.noreply@gmail.com", "name": "Balkan Ultra"},
            [{"email": athlete.email, "name": athlete.first_name}],
            "14",
            [{"email": "balkanultra@abv.bg", "name": "Rosen Rusev"}]
        )

    def test_sky_athlete_str(self):
        athlete = SkyAthlete.objects.create(**self.sky_athlete_data)
        self.assertEqual(str(athlete), 'Jane Doe')