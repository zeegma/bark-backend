from django.urls import path
from .views.lost_item_views import get_lost_items, create_lost_items, edit_lost_items, delete_lost_items

from . import views

urlpatterns = [
    path("", get_lost_items, name="getLostItems"),
    path("lost-items/", get_lost_items, name="getLostItems"),
    path("lost-items/create/", create_lost_items, name="createLostItems"),
    path("lost-items/<int:item_id>/", edit_lost_items, name="editLostItems"),
    path("lost-items/<int:item_id>/delete/", delete_lost_items, name="deleteLostItems"),
]