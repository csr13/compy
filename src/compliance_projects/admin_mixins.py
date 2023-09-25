import csv
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.views import View


class AdminExtendedActionView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.info(request, "Fuck off")
            return HttpResponseRedirect(
                reverse("fuck-off")
            )
        return super().dispatch(request, *args, **kwargs)


class CsvAdminMixin(object):
    """
    Обробка експорту моделей у CSV.
    """
    def export_framework_controls_as_csv(self, request, obj):
        try:
            meta = obj._meta
            model_name = meta.model_name
            app_name = meta.app_label
            controls = obj.controls.all()
            if controls.count() < 0:
                messages.warning(request, "This Framework has no controls")
                return HttpResponseRedirect(
                    reverse(
                        "admin:%s_%s_changelist" % (
                            app_name,
                            model_name
                        )
                    )
                )
            control_fields = [x.name for x in controls[0]._meta.fields] + ["subcontrols"]
            resp = HttpResponse(content_type='text/csv')
            file_name = "_".join(obj.name.split(" ")).lower() + "_controls.csv"
            resp['Content-Disposition'] = 'attachment; filename=%s' % file_name
            writer = csv.DictWriter(resp, fieldnames=control_fields)
            writer.writeheader()
            for control in controls:
                subcontrols = ",".join([sub.ref_code for sub in control.subcontrols.all()])
                row = {field : getattr(control, field) for field in control_fields}
                row["subcontrols"] = subcontrols
                row = writer.writerow(row)

        except Exception as error:
            if settings.DEBUG:
                raise error
                message = str(error)
            else:
                message = "Unable to process request for csv"
            messages.warning(request, message)
            return HttpResponseRedirect(
                reverse(
                    "admin:%s_%s_changelist" % (
                        app_name,
                        model_name
                    )
                )
            )
        return resp
            
