from django.urls import path

from . import views

urlpatterns = [
    path("cards/", views.list_cards, name="list-cards"),
    path("cards/<int:card_id>/", views.card_detail, name="card-detail"),
    path("cards/create/", views.create_card, name="create-card"),
    path("cards/<int:card_id>/update/", views.update_card, name="update-card"),
]
