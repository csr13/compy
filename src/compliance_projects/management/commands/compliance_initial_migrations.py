import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from compliance_projects import models



class Command(BaseCommand):
    
    help = "Loads Frameworks, policies, adds default controls to each framework."

    
    controls_path = os.path.join(
        settings.BASE_DIR, 
        "compliance_projects", 
        "files", 
        "base_controls",
    )
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
        "SAMA_CRF",
        "CIS_CSC_v6.1",
        "SOC2_2017",
        "CIS_CSC_v7",
        "CS_CCM_v3.0.1",
        "NIST_800r4",
        "NIST800_171r1",
        "NIST_CSF_v1.1",
        "OWASP_Top_10_(2017)",
        "PCI_DSS_v3.2.1",
        "FedRAMP_(Mod)",
        "FFIEC",
        "Mitre_ATT&CK",
        "HIPPA"
    ]

    def handle(self, *args, **kwargs):
       # Create Framework
        frameworks = {
            "created" : [],
            "errors" : []
        }
        for each in [x.lower() for x in self.frameworks]:
            path = os.path.join(self.controls_path, "%s_controls.json" % each)
            if not os.path.exists(path):
                self.stdout.write(
                    self.style.ERROR("%s does not exist .. continuing" % each)
                )
                continue
            name = path.strip("_controls.json")
            name = os.path.split(name)[1]
            self.stdout.write(self.style.SUCCESS("Trying framework %s" % name))
            try:
                result, framework = models.Framework.cook_framework(
                    name,
                    add_controls=True,
                    add_policies=True,
                )
                if not result:
                    raise Exception(framework)
            except Exception as error:
                frameworks["errors"].append(name + " " + str(error))
                self.stdout.write(
                    self.style.ERROR(str(error))
                )
            else:
                frameworks["created"].append(framework)
                self.stdout.write(
                    self.style.SUCCESS("Framework %s created" % name)
                )
