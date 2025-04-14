from django.urls import path
from .views.lost_item_views import get_lost_items, create_lost_items, delete_lost_items
from .views.claim_form_views import create_claim_form, get_claim_forms
from .views.admin_dashboard_views import total_items

urlpatterns = [
    path("", get_lost_items, name="getLostItems"),
    path("lost-items", get_lost_items, name="getLostItems"),
    path("lost-items/create", create_lost_items, name="createLostItems"),
    path("lost-items/<int:item_id>", delete_lost_items, name="deleteLostItems"),
    # Claim Form
    path("claim-forms", get_claim_forms, name="getClaimForms"),
    path("claim-form/create", create_claim_form, name="createClaimForm"),
    # Admin Dashboard
    path('admin/stats/total', total_items, name='total_items'),
]