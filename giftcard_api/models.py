from django.db import models

class Giftcards(models.Model):


	identifier = models.IntegerField(primary_key=True, unique=True)
	#decrease this value after each purchase.
	credit_remaining = models.IntegerField(default=25)
	#Take the current date and add a day onto it.
	expiry_date = models.DateField()

	def __str__(self):
		return self.identifier

	class Meta:
		verbose_name = "Giftcard"
		verbose_name_plural = "Giftcards"

class Scoreboard(models.Model):
	score_id = models.AutoField(primary_key=True)
	probability_heads = models.DecimalField(max_digits=3, decimal_places=2)
	probability_tails = models.DecimalField(max_digits=3, decimal_places=2)