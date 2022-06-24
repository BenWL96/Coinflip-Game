from .models import Giftcards
from django.http import Http404

class SingleFieldLookupMixin_Giftcards:
	def get_object(self):

		parameter_passed = self.kwargs
		giftcard_identifier = parameter_passed['identifier']
		print(giftcard_identifier)
		try:
			giftcard = Giftcards.objects.get(identifier=giftcard_identifier)
			self.check_object_permissions(self.request, giftcard)
			return giftcard

		except Giftcards.DoesNotExist:
			return Http404("No matches for the given query.")



