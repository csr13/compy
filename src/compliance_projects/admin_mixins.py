import csv
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
                messages.info(request, "This Framework has no controls")
                return HttpResponseRedirect(
                    reverse(
                        "admin:%s_%s_change" % (
                            model_name, 
                            app_name
                        )
                    )
                )
            control_fields = [x.name for x in controls[0]._meta.fields]
            resp = HttpResponse(content_type='text/csv')
            file_name = "_".join(obj.name.split(" ")).lower() + "_controls.csv"
            resp['Content-Disposition'] = 'attachment; filename=%s' % file_name
            writer = csv.writer(resp)
            writer.writerow(control_fields)
            for control in controls:
                row = writer.writerow(
                    [getattr(control, field) for field in control_fields]
                )
        except Exception as error:
            messages.info(request, "This Framework has no controls")
            return HttpResponseRedirect(
                reverse(
                    "admin:%s_%s_change" % (
                        model_name, 
                        app_name
                    )
                )
            )
        return resp
            
