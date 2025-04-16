from django.urls import path
from .views.lost_item_views import get_lost_items, create_lost_items, delete_lost_items
from .views.admin_views import get_admins, register_admin, admin_detail, login_admin

from . import views

urlpatterns = [
    path("", get_lost_items, name="getLostItems"),
    path("lost-items", get_lost_items, name="getLostItems"),
    path("lost-items/create", create_lost_items, name="createLostItems"),
    path("lost-items/<int:item_id>", delete_lost_items, name="deleteLostItems"),

    path("admins/", get_admins, name="getAdmins"),
    path("admins/register/", register_admin, name="registerAdmin"),
    path("admins/<int:admin_id>", admin_detail, name="deleteAdmin"),
    path("admins/login/", login_admin, name="loginAdmin")
]