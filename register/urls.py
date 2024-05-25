from . import views as register_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('', register_views.account_register, name="register"),
    path('login', register_views.login_view, name='login'),
    path('verify_email/<int:pk>', register_views.verify_email, name='verify-email'),
    path('logout', register_views.account_logout, name='logout'),
    path("dashboard", register_views.user_dashboard, name="user-dashboard"),
    path("open-orders", register_views.user_open_orders, name="user-open-orders"),
    path("buy-product/<int:product_id>/", register_views.user_buy_product, name="buy-product"),
    path('upload-file/<int:product_id>/', register_views.upload_file, name='upload-file-user'),
    path('completed-orders', register_views.completed_orders, name='completed-order-user'),
    path('success-orders/<str:slug>', register_views.success_order, name='success-order'),
    path('failed-orders/<str:slug>', register_views.failed_order, name='failed-order'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
