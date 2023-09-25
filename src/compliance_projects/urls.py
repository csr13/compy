from django.urls import path

from compliance_projects import admin_views


app_name = "compliance_projects"


urlpatterns = [
    path(
        'export-framework-controls-csv/<pk>', 
        view=admin_views.ExportFrameworkControlsToCsv.as_view(),
        name='export-framework-controls-csv'
    ),
]
