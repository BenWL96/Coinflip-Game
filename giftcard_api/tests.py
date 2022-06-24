from django.test import TestCase
from .models import Giftcards
from .utils import create_giftcard

# Create your tests here.
class test_giftcard_endpoints(TestCase):

	#Here we're just testing the error codes
	#We don't need to add anything to the database.

	def test_endpoints_and_functionality(self):
		"""API_Consultation_Endpoint"""

		giftcard_created = create_giftcard()
		print(giftcard_created)

		"""args = {
			'date': date,
			'consultation_id': consultation_id,
		}

		# PATCH

		consultation_now_booked = {"consultation_booked": True}

		url = reverse('lessons_restful:consultation-detail', kwargs=args)

		response = self.client.patch(
			url, HTTP_AUTHORIZATION='Token {}'.format(
				self.token
			), data=consultation_now_booked)

		input_dict = response.data
		response_dict = json.loads(json.dumps(input_dict))

		message_match = {
			'message': 'The details of the consultation with ID: 1 have been updated successfully'}

		if self.assertEqual(response_dict, message_match) == False:
			print("patch test failed")"""


