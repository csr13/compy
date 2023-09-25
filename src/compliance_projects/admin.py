from django.contrib import admin
from django.conf import settings
from django.utils.html import mark_safe
from django.shortcuts import reverse

from compliance_projects import models


class ProjectEvidenceInline(admin.TabularInline):
    model = models.ProjectEvidence
    extra = 1


class ControlInline(admin.TabularInline):
    model = models.Control
    extra = 1


@admin.register(models.Control)
class AdminControl(admin.ModelAdmin):
    search_fields = ["framework__name"]
    filter_horizontal = ["subcontrols"]
    list_display = [
        "pk", 
        "ref_code",
        "name", 
        "framework",
    ]


@admin.register(models.ComplianceProject)
class AdminComplianceProject(admin.ModelAdmin):
    inlines = [ProjectEvidenceInline]
    filter_horizontal = [
        "frameworks", 
        "policies"
    ]
    fieldsets = (
        (
            "Project Main Information",
            {"fields" : [
                    "user", 
                    "uuid", 
                    "name", 
                    "frameworks",
                    "policies",
                    "description", 
                    "target_level",
                ],
            "classes" : ["wide", "extrapretty"]
            }
        ),
    )
    readonly_fields = []


@admin.register(models.Policy)
class AdminPolicy(admin.ModelAdmin):
    fields = [
        "safe_content", 
        "uuid", 
        "name", 
        "ref_code", 
        "description", 
        "template"
    ] 
    readonly_fields = ["safe_content"]
    
    @admin.display(description="Policy description")
    def safe_content(self, obj):
        return mark_safe(obj.template)


@admin.register(models.Framework)
class AdminComplianceFramework(admin.ModelAdmin):
    filter_horizontal = ["controls"]
    list_display = [
        "pk", 
        "name", 
        "total_controls",
        "export_controls"
    ]
    fields = [
        "framework_guidance",
        "name",
        "description",
        "reference_link",
        "controls",
        "export_controls"
    ]
    readonly_fields = [
        "framework_guidance", 
        "export_controls"
    ]
    
    @admin.display(description="Total Controls")
    def total_controls(self, obj):
        return obj.controls.all().count()

    @admin.display(description="Framework guidance")
    def framework_guidance(self, obj):
        if obj.guidance is None:
            return mark_safe("<p>No Guidance for %s</p>" % obj.name)
        return mark_safe(obj.guidance)
    
    @admin.display(description="Export controls")
    def export_controls(self, obj):
        href_csv = reverse(
            "compliance_projects:export-framework-controls-csv",
            args=(obj.pk,)
        )
        href_json = ""
        style = """
        padding: 5px;
        margin: 5px;
        background-color: #4ac1f7;
        color: black;
        """
        return mark_safe(
            """
            <a style='%s' href='%s'>CSV</a>
            <a style='%s' href='%s' disabled>JSON</a>
            """ % (style, href_csv, style, href_json)
        )


@admin.register(models.SubControl)
class AdminSubControl(admin.ModelAdmin):
    list_display = [
        "ref_code", 
        "parent_control_framework",
        "parent_control_verbose"
    ]
    
    @admin.display(description="Parent Control")
    def parent_control_verbose(self, obj):
        if obj.parent_control:
            return obj.parent_control
        return "Add control manually."

    @admin.display(description="Parent Control Framework")
    def parent_control_framework(self, obj):
        if obj.parent_control:
            return obj.parent_control.framework
        return "No parent control, add one manually."


@admin.register(models.Evidence)
class AdminEvidence(admin.ModelAdmin):
    search_fields = ["name", "project__name"]
    filter_horizontal = ["controls"]
    list_display = ["name", "project", "solved", "created_at"]
    prepopulated_fields = {"slug" : ["name"]}


@admin.register(models.ProjectEvidence)
class AdminProjectEvidence(admin.ModelAdmin):
    list_display = ["project", "evidence"]
