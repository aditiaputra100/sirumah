
from django.test import TestCase, Client
from django.urls import reverse
from django.middleware.csrf import CsrfViewMiddleware

# Create your tests here.

class CSRFProtectionTest(TestCase):
	def setUp(self):
		self.client = Client(enforce_csrf_checks=True)

	def test_find_house_post_without_csrf(self):
		"""
		POST ke find_house tanpa CSRF token harus menghasilkan 403 Forbidden.
		"""
		url = reverse('find_house')
		response = self.client.post(url, {})
		self.assertEqual(response.status_code, 403)
	
	def test_find_house_post_with_csrf(self):
		"""
		POST ke find_house dengan CSRF token yang valid
		harus menghasilkan 200 OK (asumsi view mengembalikan 200).
		"""
		url = reverse('find_house')

		# Pertama GET untuk mendapatkan CSRF token
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

		# Ambil CSRF token dari cookie
		csrf_token = response.cookies['csrftoken'].value

		form_data = {
            'location_weight': 9,
			'price_weight': 7,
			'building_area_weight': 5,
			'land_area_weight': 3,
			'specification_weight': 1,
			'facility_weight': 1,
            'csrfmiddlewaretoken': csrf_token,
        }

		# Kirim POST dengan menyertakan CSRF token
		response = self.client.post(
			url,
			data=form_data,
			follow=True,
			HTTP_ORIGIN='http://localhost',
		)
		self.assertEqual(response.status_code, 200)
