from django.urls import path
from .views.lost_item_views import get_lost_items, create_lost_items, delete_lost_items
from .views.claim_form_views import create_claim_form

urlpatterns = [
    path("", get_lost_items, name="getLostItems"),
    path("lost-items", get_lost_items, name="getLostItems"),
    path("lost-items/create", create_lost_items, name="createLostItems"),
    path("lost-items/<int:item_id>", delete_lost_items, name="deleteLostItems"),
    path("claim-form/create", create_claim_form, name="create_claim_form"),
]