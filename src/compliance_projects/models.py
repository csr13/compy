import logging
import os
import json
import uuid
import random

from django.db import models
from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


logger = logging.getLogger(__name__)


def generate_uuid():
    return "%s-%s" % (random.randint(69,666), uuid.uuid4().hex)


def evidences_storage(instance, filename):
    return "evidences/documents/%s" % filename


class Control(models.Model):
    framework = models.ForeignKey('compliance_projects.Framework', on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, default=generate_uuid, null=True)
    name = models.TextField(default="", null=True)
    description = models.TextField(default="", null=True)
    ref_code = models.CharField(max_length=255, null=True)
    visible = models.BooleanField(default=True)
    level = models.CharField(max_length=255, null=True)
    system_level = models.BooleanField(default=True)
    category = models.TextField(default="", null=True)
    subcategory = models.TextField(default="", null=True)
    guidance = models.TextField(default="", null=True)
    references = models.TextField(default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Framework specific fields
    # ISO27001
    operational_capability = models.TextField(default="", null=True)
    control_type = models.TextField(default="", null=True)
    control_domain = models.TextField(default="", null=True)
    domain_name = models.TextField(default="", null=True)
    # HIPPA
    dti = models.CharField(max_length=255, null=True)
    dtc = models.CharField(max_length=255, null=True)
    meta = models.JSONField(default=dict, null=True)
    subcontrols = models.ManyToManyField(
        'compliance_projects.SubControl', 
        blank=True
    )
   
    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Control"
        verbose_name_plural = "Controls"

    @classmethod
    def cook_control(cls, data, framework):
        with transaction.atomic():
            data["framework"] = framework
            try:
                try:
                    subcontrols = data.pop("subcontrols")
                except Exception as error:
                    subcontrols = []
                try:
                    if data["system_level"] == "":
                        data["system_level"] = False
                except Exception as error:
                    data["system_level"] = False
                
                parent_control = Control.objects.create(**data)
            except Exception as error:
                logger.exception(str(error))
                return False, str(error)
            try:
                if len(subcontrols) > 0:
                    for each in subcontrols:
                        try:
                            subcontrol = SubControl.objects.create(**each) 
                            parent_control.subcontrols.add(subcontrol)
                            parent_control.save()
                        except Exception as error:
                            logger.info(str(error))
                            continue
            except Exception as error:
                logger.info(str(error))
            framework.controls.add(parent_control)
            framework.save()
        return True
            
    def __str__(self):
        return "Framework: %s | Contol code: %s " % (
            self.framework.name,
            self.ref_code
        )


class SubControl(models.Model):
    uuid = models.CharField(max_length=255, default=generate_uuid, null=True)
    name = models.TextField(default="", null=True) 
    description = models.TextField(default="", null=True)
    ref_code = models.CharField(max_length=255, null=True)
    mitigation = models.TextField(default="", null=True)
    guidance = models.TextField(default="", null=True)
    meta = models.JSONField(default=dict, null=True)
    # Framework specific
    implementation_group = models.IntegerField(null=True)
    parent_control = models.ForeignKey(
        'compliance_projects.Control',
        on_delete=models.CASCADE,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Sub Control"
        verbose_name_plural = "Sub Controls"

    def __str__(self):
        return self.name


class Policy(models.Model):
    uuid = models.CharField(max_length=255, default=generate_uuid, null=True)
    name = models.CharField(max_length=255, null=True)
    ref_code = models.CharField(max_length=255, null=True)
    description = models.TextField(default="", null=True)
    content = models.TextField(default="", null=True)
    template = models.TextField(default="", null=True)
    version = models.IntegerField(default=1)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

   
class Evidence(models.Model):
    uuid = models.CharField(max_length=255, default=generate_uuid, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(
        'compliance_projects.ComplianceProject',
        on_delete=models.CASCADE, 
        null=True
    )
    name = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True, unique=True)
    description = models.CharField(max_length=255, null=True)
    content = models.CharField(max_length=255, null=True)
    controls = models.ManyToManyField('compliance_projects.Control', blank=True)
    document = models.FileField(upload_to=evidences_storage, null=True)
    solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
     
    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Evidence"
        verbose_name_plural = "Evidences"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @classmethod
    def cook_evidence(cls, **data):
        user = data["user"]
        project = data["project"]
        name = data["name"]
        if cls.objects.filter(
            user=user, 
            project=project, 
            name=name,
        ).exists():
            return False, "Exact evidence exists."
        try:
            cls.objects.create(**data)
        except Exception as error:
            return False, "Unable to create evidence."
        return True, "Evidence created."
    
    def __str__(self):
        return "Project: %s | Evidence: %s" % (
            self.project.name, 
            self.name
        )


class Framework(models.Model):
    uuid = models.CharField(max_length=255, default=generate_uuid, null=True)
    name = models.TextField(default="", blank=True)
    description = models.TextField(default="", null=True)
    reference_link = models.TextField(default="", blank=True, null=True)
    guidance = models.TextField(default="", blank=True, null=True)
    #####################################
    # Framework Specific features
    #####################################
    controls = models.ManyToManyField(
        'compliance_projects.Control', 
        related_name="framework_controls",
        blank=True
    )
    feature_evidence = models.BooleanField(default=bool(0))
    created_at = models.DateTimeField(auto_now_add=bool(1))

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Framework"
        verbose_name_plural = "Frameworks"
 
    @classmethod
    def get_valid_frameworks(cls):
        frameworks = [
            "soc2",
            "cmmc",
            "iso27001",
            "hipaa",
            "nist_800_53_v4",
            "nist_csf_v1.1",
            "asvs_v4.0.1",
            "ssf",
            "cisv8",
            "pci_3.1",
            "201_CMR_17",
            "AADHAAR_Act",
            "Australia_APRA_cpg_234", 
            "Canada", 
            "CIS_Controls_V7.1", 
            "Controls_Mapping", 
            "FFIEC", 
            "Final_Rule_Privacy", 
            "GDPR", 
            "HIPPA_HITRUST", 
            "HITRUST_CSF", 
            "hongkong_SFC_internet_trading", 
            "Identity_Theft_Red_flags", 
            "ISO_22301", 
            "ISO_27001_Requirements", 
            "ISO_27001", 
            "ISO_27002", 
            "IT_Act_India", 
            "MAS_TRM_Guidelines", 
            "NIST_800_53", 
            "NIST_800_171", 
            "NIST_SP_800_53_Revision_5", 
            "NYCRR", 
            "PCI_DSS_v3.2.1", 
            "Qutar_NIA_Manual", 
            "Regulation_S_AM", 
            "SAMA_CRF"
        ]
        return [x.lower() for x in frameworks]

    @classmethod
    def check_valid_framework(cls, name):
        if name not in cls.get_valid_frameworks():
            return False
        return True
 
    @classmethod
    def cook_framework(cls, name, add_controls=False, add_policies=False):
        if not cls.check_valid_framework(name):
            return False, "Invalid framework %s" % name
        data = {
            "name" : name,
            "description" : f"Framework for {name.upper()}",
            "feature_evidence" : bool(1),
        }
        path = os.path.join(
            settings.BASE_DIR, 
            "compliance_projects", 
            "files",
            "about_frameworks",
            f"{name}.html"
        )
        logger.info("Checking for framework guidance file %s" % path)
        if os.path.exists(path):
            with open(path) as f:
                guidance = f.read()
                data["guidance"] = guidance
        try:
            if cls.objects.filter(**data).exists():
                raise Exception(
                    "Framework %s exists" % data["name"]
                ) from None
            framework = cls.objects.create(**data)
        except Exception as error:
            logger.error(str(error))
            return False, str(error)

        if add_controls: cls.create_base_controls(name, framework)
        if add_policies: cls.create_base_policies()

        return True, framework

    @classmethod
    def create_base_controls(cls, name, framework):
        path = os.path.join(
            settings.BASE_DIR, 
            "compliance_projects", 
            "files",
            "base_controls",
            "%s_controls.json" % name
        )
        with open(path) as f:
            controls=json.load(f)
            for each in controls:
                try:
                    operation = Control.cook_control(each, framework)
                    if not operation:
                        raise Exception("Unable to create")
                except Exception as error:
                    logger.exception(str(error))
                    continue
                logger.info("Created control: %s for framework: %s" % (
                        name, 
                        framework.name
                    )
                )
        return True

    @classmethod
    def create_base_policies(cls):
        policies_path = os.path.join(
            settings.BASE_DIR,
            "compliance_projects",
            "files",
            "base_policies"
        )
        for filename in os.listdir(policies_path):
            if not filename.endswith(".html"):
                continue
            policy_path = os.path.join(policies_path, filename)
            with open(policy_path) as f:
                name = filename.split(".")[0]
                content = f.read()
            with transaction.atomic():
                if Policy.objects.filter(name=name).exists():
                    continue
                else:
                    Policy.objects.create(
                        name=name,
                        description=f"Content for the {name} policy",
                        content=content,
                        template=content
                    )
                pass
            continue
        return True

    def __str__(self):
        return " ".join(self.name.split("_"))

    def __repr__(self):
        return self.name
   

class ComplianceProjectTag(models.Model):
    uuid = models.CharField(max_length=255, default=generate_uuid, null=True)
    name = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Compliance Project Tag"
        verbose_name_plural = "Compliance Project Tags"

    def __str__(self):
        return self.name
        

class ComplianceProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, default=generate_uuid, null=True)
    name = models.CharField(max_length=255, blank=False, null=True)
    slug = models.CharField(max_length=255, null=True, unique=True)
    description = models.CharField(max_length=255, null=True)
    target_level = models.IntegerField(default=1)
    frameworks = models.ManyToManyField('compliance_projects.Framework', blank=True)
    policies = models.ManyToManyField('compliance_projects.Policy', blank=True)
    evidences = models.ManyToManyField('compliance_projects.Evidence', blank=True)
    tags = models.ManyToManyField('compliance_projects.ComplianceProjectTag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Compliance Project"
        verbose_name_plural = "Compliance Projects"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProjectEvidence(models.Model):
    project = models.ForeignKey(
        'compliance_projects.ComplianceProject',
        on_delete=models.CASCADE,
        null=True
    )
    evidence = models.ForeignKey(
        'compliance_projects.Evidence',
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Project Evidence"
        verbose_name_plural = "Project Evidences"

    @classmethod
    def cook_evidence(cls, user, project, evidence):
        if cls.objects.filter(project=project, evidence=evidence).exists():
            return False, "This evidence already exists."
        if project.evidences.filter(evidence=evidence).exists():
            return False, "This evidence already exists in this project."
        try:
            project_evidence = cls.objects.create(
                project=project, 
                evidence=evidence
            )
        except Exception as error:
            return False, "Unable to create project evidence"
        try:
            project.evidences.add(evidence)
        except Exception as error:
            return False, "Unable to add evidence to project evidences."
        return True, "Project evidence relation created,added to project evidences."    

    @classmethod
    def delete_project_evidence(cls, project, evidence):
        try:
            cls.objects.filter(project=project, evidence=evidence).delete()
        except Exception as error:
            logger.error(str(error))
            return False, "Unable to delete project evidence"
        return True, "Project evidence deleted."

    def __str__(self):
        evidence = self.evidence.description
        project_name = self.project.name
        return "%s - %s" % (project_name, evidence)
   

class PolicyControl(models.Model):
    policy = models.ForeignKey(
        'compliance_projects.Policy', 
        on_delete=models.CASCADE,
        null=True
    )
    control = models.ForeignKey(
        'compliance_projects.Control',
        on_delete=models.CASCADE,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Policy Control"
        verbose_name_plural = "Policy Controls"

    def __str__(self):
        return "%s %s" % (
            self.policy.name, 
            self.control.ref_code,
            self.control.parent_framework.name
        )
