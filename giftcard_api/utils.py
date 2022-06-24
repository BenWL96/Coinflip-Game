import random
import datetime
from .models import (
	Giftcards
)

def create_giftcard():
	print("HUH")

	flag = False

	print("Identifier has been selected")

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