import io
from django.conf import settings
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from unittest import mock
from sib_api_v3_sdk.rest import ApiException

from app.models import SkyAthlete, UltraAthlete
from app.views import athletes_view, download_gpx_view, register_view


class MockMailResult:
    def __init__(self, value):
        self.value = value

    def to_str(self):
        return self.value

class AthletesViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.ultra_gpx_content = b'<gpx>ultra race data</gpx>'
        self.sky_gpx_content = b'<gpx>sky race data</gpx>'

        self.sky_athlete1 = SkyAthlete.objects.create(
            first_name="Gosho",
            last_name="Georgiev",
            phone="08888888",
            email="abv@abv.bg",
            gender="male"
            
        )
        self.sky_athlete2 = SkyAthlete.objects.create(
            first_name="Ivanka",
            last_name="Ivanova",
            phone="088777777",
            email="yahoo@abv.bg",
            gender="female"
        )

        self.ultra_athlete1 = UltraAthlete.objects.create(
            first_name="Rosen",
            last_name="Rosenov",
            phone="029949124",
            email="roskata@abv.bg",
            gender="male",
            paid=True

        )
        self.ultra_athlete2 = UltraAthlete.objects.create(
            first_name="Mariq",
            last_name="Ivanova",
            phone="044401213",
            email="mariika@abv.bg",
            gender="female",
            paid=False
        )

        self.ultra_data = {
            'first_name': 'Horhe',
            'last_name': 'Bukai',
            'email': 'ultra@example.com',
            'gender': 'male',
            'phone': '0848822432',
            'first_link': 'racetiming.net/race-results.pdf',
            'second_link': 'results.bg/results.csv'
        }
        self.sky_data = {
            'first_name': 'Stoqn',
            'last_name': 'Kolev',
            'email': 'sky@example.com',
            'phone': '0299412312',
            'gender': 'male',
        }

    def test_athletes_view_returns_all_sky_athletes(self):
        request = self.factory.get(reverse('athletes'))
        response = athletes_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.sky_athlete1.first_name)
        self.assertContains(response, self.sky_athlete2.first_name)

    def test_athletes_view_returns_only_paid_ultra_athletes(self):
        request = self.factory.get(reverse('athletes'))
        response = athletes_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ultra_athlete1.first_name)
        self.assertNotContains(response, self.ultra_athlete2.first_name)

    @mock.patch('app.views.get_gpx_file')
    def test_download_gpx_view_returns_ultra_gpx_file(self, mock_get_gpx_file):
        mock_get_gpx_file.return_value = io.BytesIO(self.ultra_gpx_content)
        request = self.factory.get(reverse('download', args=['ultra']))
        response = download_gpx_view(request, 'ultra')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.ultra_gpx_content)
        self.assertEqual(response['Content-Type'], 'application/gpx+xml')
        self.assertEqual(response['Content-Disposition'], 'inline; filename=balkan_ultra.gpx')

    @mock.patch('app.views.get_gpx_file')
    def test_download_gpx_view_returns_sky_gpx_file(self, mock_get_gpx_file):
        mock_get_gpx_file.return_value = io.BytesIO(self.sky_gpx_content)
        request = self.factory.get(reverse('download', args=['sky']))
        response = download_gpx_view(request, 'sky')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, self.sky_gpx_content)
        self.assertEqual(response['Content-Type'], 'application/gpx+xml')
        self.assertEqual(response['Content-Disposition'], 'inline; filename=balkan_sky.gpx')

    def test_registration_disabled(self):
        settings.REGISTRATION_ENABLED = False
        url = reverse("register", kwargs={"race": "ultra"})
        resp = self.client.post(url, {})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "disabled_register.html")

    def test_registration_enabled(self):
        settings.REGISTRATION_ENABLED = True
        url = reverse('register', args=['ultra'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'register.html')
    
    def test_register_ultra_athlete(self):
        settings.REGISTRATION_ENABLED = True
        url = reverse('register', args=['ultra'])
        response = self.client.post(url, self.ultra_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UltraAthlete.objects.filter(email=self.ultra_data['email']).exists())
    
    def test_register_sky_athlete(self):
        settings.REGISTRATION_ENABLED = True
        url = reverse('register', args=['sky'])
        response = self.client.post(url, self.sky_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SkyAthlete.objects.filter(email=self.sky_data['email']).exists())

    def test_register_existing_athlete(self):
        settings.REGISTRATION_ENABLED = True
        ultra_athlete = UltraAthlete.objects.create(**self.ultra_data)
        response = self.client.post(reverse('register', args=['ultra']), self.ultra_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')
        
    @mock.patch('app.models.UltraAthlete.send_mail')    
    def test_register_ultra_athlete_mail_service(self, mock_send_mail):
        settings.REGISTRATION_ENABLED = True
        mock_send_mail.return_value =  MockMailResult('mail_sent')
        url = reverse('register', args=['ultra'])
        response = self.client.post(url, self.ultra_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['mail_status'], 'success')
        self.assertEqual(response.json()['mail_error'], None)
        self.assertTrue(UltraAthlete.objects.filter(email=self.ultra_data['email']).exists())

    @mock.patch('app.models.SkyAthlete.send_mail')
    def test_send_mail_api_exception(self, mock_send_mail):
        mock_send_mail.side_effect = ApiException('API error', 'Failure')
        response = self.client.post(reverse('register', args=['sky']), self.sky_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['mail_status'], 'error')
        self.assertEqual(response.json()['mail_error'], '(API error)\nReason: Failure\n')
