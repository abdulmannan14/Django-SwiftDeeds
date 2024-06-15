import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from . import models as admin_models
from register import models as register_models


class AllVerifiedUsersTable(tables.Table):
    # connector_name = tables.Column(empty_values=())
    email = tables.Column(empty_values=())
    user = tables.Column(verbose_name='username')

    # send_mail = tables.Column(empty_values=())

    # send_mail = tables.Column(empty_values=())

    def render_email(self, record):
        record: register_models.UserProfile
        return record.user.email

    # def render_send_mail(self, record):
    #     return format_html("""
    #     <a class='btn btn-sm text-warning email-btn'  href='{id}' onclick='send_mail_and_sms(this)'><i class='fa fa-paper-plane'></i></a>
    #     """.format(
    #         id=reverse("resend-email", kwargs={"id": record.user.id})
    #     ))

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = register_models.UserProfile
        fields = ['user', 'email', ]


class ProductsTableAdmin(tables.Table):
    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = admin_models.Products
        fields = ['name', 'price', 'description']

    def render_price(self, value):
        return format_html('${}', value)


class ProductsTable(tables.Table):
    buy = tables.Column(empty_values=())  # Define the custom column

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = admin_models.Products
        fields = ['name', 'price', 'description']

    def render_buy(self, record):
        # Assuming there's a URL pattern named 'buy-product' that takes a product ID
        buy_url = reverse('buy-product', kwargs={'product_id': record.id})
        return format_html(
            "<a class='btn btn-sm btn-primary' href='{}'>Buy</a>",
            buy_url
        )

    def render_price(self, value):
        return format_html('${}', value)


class OpenProductsTable(tables.Table):
    add_file = tables.Column(empty_values=(), verbose_name='Add Files')  # Define the custom column
    uploaded_files = tables.Column(empty_values=(), verbose_name='Uploaded Files')  # Define the custom column
    product_price = tables.Column(verbose_name='Price', empty_values=())  # Custom column for Product price
    product_description = tables.Column(verbose_name='Description',
                                        empty_values=())  # Custom column for Product description
    created_at = tables.Column(verbose_name='Created On', empty_values=())  # Custom column for Product description

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = admin_models.UserProducts
        fields = ['product', 'product_price', 'product_description', 'is_completed', 'created_at', 'completed_on']

    def render_uploaded_files(self, record):
        files = record.files.all()
        new_files = ''
        if files:
            for file in files:
                new_files += "{} <br>".format(str(file).split('/')[-1])
        return format_html(new_files)

    def render_add_file(self, record):
        # Assuming there's a URL pattern named 'upload-file' that handles file uploads
        upload_url = reverse('upload-file-user', kwargs={'product_id': record.product_id})
        return format_html(
            "<button class='btn btn-sm btn-primary' onclick='addFile({})'>Add Files</button>",
            record.id
        )

    def render_product_price(self, record):
        return format_html('${}', record.product.price)  # Access price field of the related Product

    def render_product_description(self, record):
        return record.product.description  # Access description field


class OpenOrders(tables.Table):
    add_file = tables.Column(empty_values=())  # Define the custom column
    product_price = tables.Column(verbose_name='Price', empty_values=())  # Custom column for Product price
    product_description = tables.Column(verbose_name='Description',
                                        empty_values=())  # Custom column for Product description
    created_at = tables.Column(verbose_name='Created On', empty_values=())  # Custom column for Product description

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = admin_models.UserProducts
        fields = ['product', 'product_price', 'product_description', 'is_completed', 'created_at', 'completed_on']

    def render_add_file(self, record):
        # Assuming there's a URL pattern named 'upload-file' that handles file uploads
        upload_url = reverse('upload-file-user', kwargs={'product_id': record.id})
        return format_html(
            "<button class='btn btn-sm btn-primary' onclick='addFile({})'>Add</button>",
            record.product_id
        )

    def render_product_price(self, record):
        return format_html('${}', record.product.price)  # Access price field of the related Product

    def render_product_description(self, record):
        return record.product.description  # Access description field


class CompletedProductsTable(tables.Table):
    see_files = tables.Column(empty_values=())  # Define the custom column
    view_report = tables.Column(empty_values=())  # Define the custom column
    product_number = tables.Column(verbose_name='Product Number', empty_values=()) # Custom column for product number
    product_price = tables.Column(verbose_name='Price', empty_values=())  # Custom column for Product price
    product_description = tables.Column(verbose_name='Description',
                                        empty_values=())  # Custom column for Product description
    created_at = tables.Column(verbose_name='Created On', empty_values=())  # Custom column for Product description


    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = admin_models.UserProducts
        fields = ['product', 'user', 'product_number', 'product_price', 'product_description', 'is_completed', 'created_at', 'completed_on']

    def render_product_number(self, record):
        return record.id
    
    def render_product_price(self, record):
        return format_html('${}', record.product.price)  # Access price field of the related Product

    def render_product_description(self, record):
        return record.product.description  # Access description field

    def render_see_files(self, record):
        # Assuming there's a URL pattern named 'upload-file' that handles file uploads
        upload_url = reverse('upload-file-user', kwargs={'product_id': record.product_id})
        return format_html(
            "<button class='btn btn-sm btn-primary' onclick='ShowFileModal({product_id})'>View</button>",
            product_id=record.id
        )

    def render_view_report(self, record):
        if record.completed_final_file:
            return format_html(
                "<a class='btn btn-sm btn-primary' target=blank href={}>View Report</a>",
                record.completed_final_file.url

            )
        return "No Report yet"


class OpenOrdersAdmin(tables.Table):
    see_files = tables.Column(empty_values=())  # Define the custom column
    approve_order = tables.Column(empty_values=())  # Define the custom column
    product_number = tables.Column(verbose_name='Product Number', empty_values=()) # Custom column for product number
    product_price = tables.Column(verbose_name='Price', empty_values=())  # Custom column for Product price
    product_description = tables.Column(verbose_name='Description',
                                        empty_values=())  # Custom column for Product description
    created_at = tables.Column(verbose_name='Created On', empty_values=())  # Custom column for Product description

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = admin_models.UserProducts
        fields = ['product', 'user', 'product_number', 'product_price', 'product_description', 'is_completed', 'created_at', 'completed_on']

    def render_product_number(self, record):
        return record.id
    
    def render_see_files(self, record):
        # Assuming there's a URL pattern named 'upload-file' that handles file uploads
        upload_url = reverse('upload-file-user', kwargs={'product_id': record.product_id})
        return format_html(
            "<button class='btn btn-sm btn-primary' onclick='ShowFileModal({product_id})'>View</button>",
            product_id=record.id
        )

    def render_product_price(self, record):
        return format_html('${}', record.product.price)  # Access price field of the related Product

    def render_product_description(self, record):
        return record.product.description  # Access description field

    def render_approve_order(self, record):
        return format_html(
            "<button class='btn btn-sm btn-success' onclick='approveOrder({product_id})'>Approve Order</button>",
            product_id=record.id
        )


class CompletedProductsTableUser(tables.Table):
    see_files = tables.Column(empty_values=())  # Define the custom column
    view_report = tables.Column(empty_values=())  # Define the custom column
    product_price = tables.Column(verbose_name='Price', empty_values=())  # Custom column for Product price
    product_description = tables.Column(verbose_name='Description',
                                        empty_values=())  # Custom column for Product description
    created_at = tables.Column(verbose_name='Created On', empty_values=())  # Custom column for Product description

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = admin_models.UserProducts
        fields = ['product', 'product_price', 'product_description', 'is_completed', 'created_at', 'completed_on']

    def render_product_price(self, record):
        return format_html('${}', record.product.price)  # Access price field of the related Product

    def render_product_description(self, record):
        return record.product.description  # Access description field

    def render_see_files(self, record):
        # Assuming there's a URL pattern named 'upload-file' that handles file uploads
        upload_url = reverse('upload-file-user', kwargs={'product_id': record.product_id})
        return format_html(
            "<button class='btn btn-sm btn-primary' onclick='ShowFileModal({product_id})'>View</button>",
            product_id=record.id
        )

    def render_view_report(self, record):
        return format_html(
            "<a class='btn btn-sm btn-primary' target=blank href={}>View Report</a>",
            record.completed_final_file.url

        )
