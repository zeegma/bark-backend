from django.urls import path
from .views.lost_item_views import (
    get_lost_items,
    get_lost_item,
    create_lost_items,
    edit_lost_items,
    delete_lost_items
)
from .views.admin_views import get_admins, register_admin, admin_detail, login_admin, delete_admin, logout_admin

from .views.claim_form_views import create_claim_form, get_claim_forms, delete_claim_forms
from .views.admin_dashboard_views import (
    total_items,
    lost_items,
    claimed_items,
    expired_items,
    dashboard_stats
)

urlpatterns = [
    # Lost Items
    path("", get_lost_items, name="getLostItems"),
    path("lost-items/", get_lost_items, name="getLostItems"),
    path("lost-items/<int:item_id>/", get_lost_item, name="getLostItem"),
    path("lost-items/create/", create_lost_items, name="createLostItems"),
    path("lost-items/<int:item_id>/edit/", edit_lost_items, name="editLostItems"),
    path("lost-items/<int:item_id>/delete/", delete_lost_items, name="deleteLostItems"),

    path("admins/", get_admins, name="getAdmins"),
    path("admins/register/", register_admin, name="registerAdmin"),
    path("admins/<int:admin_id>/", admin_detail, name="getAdminDetail"),
    path("admins/login/", login_admin, name="loginAdmin"),
    path("admins/<int:admin_id>/delete/", delete_admin, name="deleteAdmin"),
    path("admins/logout/", logout_admin, name="logoutAdmin"),

    # Claim Form
    path("claim-forms/", get_claim_forms, name="getClaimForms"),
    path("claim-form/create/", create_claim_form, name="createClaimForm"),
    path('claimants/delete/', delete_claim_forms, name='deleteClaimForms'),


    # Admin Dashboard
    path("admin/dashboard/", dashboard_stats, name="dashboardStats"),
    path("admin/stats/total/", total_items, name="totalItems"),
    path("admin/stats/lost/", lost_items, name="lostItems"),
    path("admin/stats/claimed/", claimed_items, name="claimedItems"),
    path("admin/stats/expired/", expired_items, name="expiredItems"),
]
