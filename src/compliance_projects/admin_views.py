from django.shortcuts import get_object_or_404

from compliance_projects.admin_mixins import (
    AdminExtendedActionView,
    CsvAdminMixin
)
from compliance_projects.models import Framework


class ExportFrameworkControlsToCsv(
    CsvAdminMixin,
    AdminExtendedActionView
):

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Framework, pk=kwargs["pk"])
        return self.export_framework_controls_as_csv(request, obj)     
