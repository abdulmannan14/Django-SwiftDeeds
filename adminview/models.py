from django.db import models


# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    file = models.FileField(upload_to='user_product_files/')  # Define the file field

    def __str__(self):
        return self.file.name


class UserProducts(models.Model):
    user = models.ForeignKey('register.UserProfile', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    files = models.ManyToManyField('UploadedFile', blank=True)  # Add a ManyToManyField for files
    completed_final_file = models.FileField(upload_to='user_product_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user.username
