from django.urls import path, reverse

from . import views as admin_views

urlpatterns = [
    path("users", admin_views.all_verified_users, name="admin-dashboard-verified-users"),
    path("products", admin_views.all_products, name="admin-dashboard-non-verified-users"),
    # path("add-new-admin", admin_views.add_new_admin, name="add-new-admin"),
    path("resend_email/<str:id>", admin_views.resend_email, name="resend-email"),
    path("open-orders", admin_views.open_orders, name="open-orders"),
    path("fetch-files-admin/", admin_views.fetch_files, name="fetch-files-admin"),
    path("approve-order/", admin_views.approve_order, name="approve-order"),
    path("completed-order-admin/", admin_views.completed_order, name="completed-order-admin"),
]
