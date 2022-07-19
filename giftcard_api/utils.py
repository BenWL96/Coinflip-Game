import random
import datetime
from .models import (
	Giftcards,
	Scoreboard
)
from rest_framework.response import Response
from django.http import Http404
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
def create_giftcard():

	flag = False

	while flag == False:


		identifier = random.randint(1, 2147483647)
		print("Identifier has been selected")

		try:
			giftcard = Giftcards.objects.get(identifier=identifier)

			# giftcard exists so try again!

			flag = False

		except Giftcards.DoesNotExist:

			#giftcard with generated identifier does not exist
			#make new giftcard

			tomorrows_date = datetime.date.today() + datetime.timedelta(days=1)
			credit = 25

			new_giftcard = Giftcards.objects.create(
				identifier=identifier,
				expiry_date=tomorrows_date,
				credit_remaining=credit
			)

			# return identifier and set user copy address down.

			print("a new giftcard has been made")
			flag = True


	return new_giftcard

def get_giftcard_using_id(identifier):

	try:
		giftcard = Giftcards.objects.get(identifier=identifier)
		return giftcard

	except Giftcards.DoesNotExist:
		raise Http404("No matches for the given query.")

def determine_response_by_credit_quantity(giftcard, credit_remaining):

	if credit_remaining > 0 and credit_remaining <= 25:

		activity_cost = 1
		giftcard.credit_remaining = credit_remaining - activity_cost
		giftcard.save()

		print("credit was successfull saved")

		return Response(
			{"message": "Thanks for playing ! Remaining balance : £" + str(
				giftcard.credit_remaining),
			 'credit_remaining': giftcard.credit_remaining
			 })


	elif credit_remaining == 0:
		raise Http404(
			"Sorry you have run out of credit, please redeem your card.")

	elif credit_remaining >= 25:
		raise Http404("Sorry, something went wrong here.")

def request_data_create_scoreboard_object(request):

	#score_id gets created here.
	if len(request.data) == 2:

		probability_heads = request.data['probability_heads']
		probability_tails = request.data['probability_tails']

		#Test datatype passed
		try:
			float(probability_heads) and float(probability_tails)
			print("the data passed can be converted to float")
		except (ValueError, TypeError) as e:
			raise PermissionDenied


		#convert data passed

		sum = float(probability_heads) + float(probability_tails)
		print(sum)

		#make sure sum of data is legitimate.
		#probabilities must add to 1.

		if sum == float(1.00):
			try:
				new_scoreboard_object = Scoreboard.objects.create(
					probability_heads=probability_heads,
					probability_tails=probability_tails
				)
				print("new object has been created")
			except:
				"""This isn't working"""
				raise ValidationError(e)

			return new_scoreboard_object

		print(sum)
		return {'message': "Sorry but the probability does not add to one.."}

	else:
		raise ValidationError({'message': "Sorry but this only takes dict containing probability_heads and probability_tails."})



