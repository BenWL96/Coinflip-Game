from .models import (
	Giftcards
)
from rest_framework import serializers

class SerializeGiftcards_GET(serializers.ModelSerializer):
	class Meta:
		model = Giftcards
		fields = ['identifier']

class SerializeGiftcards_POST(serializers.ModelSerializer):
	class Meta:
		model = Giftcards
		fields = '__all__'

class SerializeGiftcards_Detail(serializers.ModelSerializer):
	class Meta:
		model = Giftcards
		fields = '__all__'