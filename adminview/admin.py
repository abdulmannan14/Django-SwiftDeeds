from django.contrib import admin

# Register your models here.
from . import models as admin_models

admin.site.register(admin_models.Products)
admin.site.register(admin_models.UserProducts)
admin.site.register(admin_models.UploadedFile)
