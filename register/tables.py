import django_tables2 as tables
from . import models as account_models
from LabProj import constants as backend_constants


class UserTable(tables.Table):
    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = account_models.UserProfile
        fields = backend_constants.account_fields
