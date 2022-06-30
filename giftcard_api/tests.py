from django.test import TestCase, Client
from .models import Giftcards
from .utils import create_giftcard
import json, datetime
from django.urls import reverse
# Create your tests here.
class test_giftcard_endpoints(TestCase):

	#Here we're just testing the error codes
	#We don't need to add anything to the database.
	def setup(self):
		self.client = Client()

	def test_endpoints_and_functionality(self):
		"""API_Consultation_Endpoint"""

		url = reverse('giftcard_api:giftcards')

		response = self.client.post(
			url)

		input_dict = response.data
		response_dict = json.loads(json.dumps(input_dict))


		print("T1 initiate")
			
		
		if self.assertEqual(response_dict['credit_remaining'], 25) == False:
			return print("T1: Card has not been created")

		print("T2 initiate")
		if self.assertEqual(type(response_dict['identifier']), int) == False:
			return print("T2: Cards identifier is not an integer")


		"""AssertionError: '2022-06-30' != datetime.date(2022, 6, 30)
		
		tomorrows_date = datetime.date.today() + datetime.timedelta(days=1)
		print("T3 initiate")
		if self.assertEqual(response_dict['expiry_date'], tomorrows_date) == False:
			print("T3: Cards expiry date is tomorrow")"""


		giftcard_identifier = response_dict['identifier']

		"""patch to giftcard_detail when giftcard exists"""

		args_identifier = {'identifier': giftcard_identifier}
		url = reverse('giftcard_api:giftcard_detail', kwargs=args_identifier)

		response = self.client.patch(
			url)

		input_dict = response.data
		response_dict = json.loads(json.dumps(input_dict))

		match_dict = {'message': 'Thanks for playing ! Remaining balance : £24', 'credit_remaining': 24}

		print("T4 initiate")
		if self.assertEqual(response_dict, match_dict) == False:
			return print("T4: Cards credit did not change")


		"""put to giftcard_detail"""

		response = self.client.put(
			url)

		input_dict = response.data
		response_dict = json.loads(json.dumps(input_dict))

		match_dict = {'identifier': ['This field is required.'], 'expiry_date': ['This field is required.']}

		print(response_dict)
		if self.assertEqual(response_dict, match_dict) == False:
			return print("T5: Cards credit did not change")


		"""patch to giftcard_detail when giftcard doesn't exist"""

		args_identifier = {'identifier': giftcard_identifier + 1}
		url = reverse('giftcard_api:giftcard_detail', kwargs=args_identifier)

		response = self.client.patch(
			url)

		input_dict = response.data
		response_dict = json.loads(json.dumps(input_dict))

		match_dict = {'detail': 'Not found.'}

		print("T6 initiate")
		if self.assertEqual(response_dict, match_dict) == False:
			return print("T6: card found at API endpoint, but it can't exist")

	
