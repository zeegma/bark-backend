from django.urls import path
from .views.lost_item_views import get_lost_items, delete_lost_items

from . import views

urlpatterns = [
    path("", get_lost_items, name="getLostItems"),
    path("dashboard", get_lost_items, name="getLostItems"),
    path("lost-items/<int:item_id>", delete_lost_items, name="deleteLostItems"),
]