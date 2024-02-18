from django.urls import path
from main.views import landing_page, voting_page, thank_you
urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('vote/', voting_page, name='voting_page'),
    path('thank-you/', thank_you, name='thank_you'),
]
