
from django.shortcuts import render
from django.http import JsonResponse

from .models import (
	Giftcards,
	Scoreboard
)

from .serializers import (
	SerializeGiftcards_GET,
	SerializeGiftcards_POST,
	SerializeGiftcards_Detail,

	SerializeScoreboard
)

from .mixins import SingleFieldLookupMixin_Giftcards

from .utils import create_giftcard

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'giftcards': '/giftcards/',
		'giftcard detail': '/giftcards/<int:identifier>/details/',

		'scoreboard': '/scoreboard/',
	}
	return Response(api_urls)

#get / post for giftcard list
@api_view(['GET', 'POST'])
def giftcard_list(request):

	if request.method == 'GET':
		giftcard = Giftcards.objects.all()
		serializer = SerializeGiftcards_GET(
			giftcard, many=True
		)
		return Response(serializer.data)

	#on button push, post and create new gift card.
	elif request.method == 'POST':

		# throttle post requests to 1 a minute.
		print("method is post")

		new_giftcard = create_giftcard()


		serializer = SerializeGiftcards_POST(
			new_giftcard, many=False
		)

		#serialize message into a dictionary before passing
		# it back into the view

		return Response(serializer.data)

#patch for giftcard detail view.


class giftcard_detail(SingleFieldLookupMixin_Giftcards,
	RetrieveUpdateAPIView):

	queryset = Giftcards.objects.all()
	serializer_class = SerializeGiftcards_Detail
	lookup_fields = ['identifier']

	def patch(self, request, *args, **kwargs):

		#If we only rely on url param, then somebody could just guess
		#an ID. If they are success, they would be able to spend money
		#That doesn't belong to them.

		# We must pass data through serializers 100%

		# Once customer pays with card, credit_remaining is reduced
		# depending on the price of the activity
		# only url parameter is depended on

		parameter_passed = self.kwargs
		identifier = parameter_passed['identifier']

		try:
			giftcard = Giftcards.objects.get(identifier=identifier)

		except Giftcards.DoesNotExist:
			raise Http404("No matches for the given query.")

		credit_remaining = giftcard.credit_remaining

		if credit_remaining > 0 and credit_remaining <= 25:

			activity_cost = 1
			giftcard.credit_remaining = credit_remaining - activity_cost
			giftcard.save()

			print("credit was successfull saved")
			print("credit was successfull saved")

			return Response({"message": "Thanks for playing ! Remaining balance : £" + str(
								 giftcard.credit_remaining),
							 'credit_remaining':  giftcard.credit_remaining
							 })


		elif credit_remaining == 0:
			raise Http404("Sorry you have run out of credit, please redeem your card.")

		elif credit_remaining >= 25:
			raise Http404("Sorry, something went wrong here.")


@api_view(['GET', 'POST'])
def scoreboard(request):

	#Always display the top 3 scores on the page.

	if request.method == 'GET':

		#only pass the top three to view.
		scoreboard = Scoreboard.objects.all()

		serializer = SerializeScoreboard(
			scoreboard, many=True
		)
		return Response(serializer.data)

	#on button push, post and create new gift card.
	elif request.method == 'POST':

		# score data posted here.

		print("method is post")
		print(request.data)
		probability_heads = request.data['probability_heads']
		probability_tails = request.data['probability_tails']

		new_scoreboard_object = Scoreboard.objects.create(
			probability_heads=probability_heads,
			probability_tails=probability_tails
		)

		serializer = SerializeScoreboard(
			new_scoreboard_object, many=False
		)

		#serialize message into a dictionary before passing
		# it back into the view

		return Response(serializer.data)
