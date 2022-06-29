
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

from .utils import (
	create_giftcard,
	get_giftcard_using_id,
	determine_response_by_credit_quantity,
	request_data_create_scoreboard_object
)

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

		print("method is post")

		new_giftcard = create_giftcard()

		serializer = SerializeGiftcards_POST(
			new_giftcard, many=False
		)

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

		giftcard = get_giftcard_using_id(identifier)

		credit_remaining = giftcard.credit_remaining

		response = determine_response_by_credit_quantity(giftcard, credit_remaining)

		return response



@api_view(['GET', 'POST'])
def scoreboard(request):

	if request.method == 'GET':

		#only pass the top three to view.
		scoreboard = Scoreboard.objects.all()

		serializer = SerializeScoreboard(
			scoreboard, many=True
		)
		return Response(serializer.data)

	elif request.method == 'POST':

		# score data posted here.

		print("method is post")

		new_scoreboard_object = request_data_create_scoreboard_object(request)

		serializer = SerializeScoreboard(
			new_scoreboard_object, many=False
		)

		return Response(serializer.data)
