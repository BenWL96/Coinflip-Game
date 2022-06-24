from django.urls import path
from . import views

app_name = "giftcard_api"

urlpatterns = [
	path('', views.apiOverview, name='overview'),
    path('giftcards/', views.giftcard_list, name="giftcards"),
	path(
		'giftcards/<int:identifier>/details/',
		views.giftcard_detail.as_view(),
		name="giftcard_detail"
	)
]