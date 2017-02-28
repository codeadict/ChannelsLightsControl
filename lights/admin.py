from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db.models import IntegerField
from django.forms import widgets

from .models import Light


def light_switch_field(field):
    def _f(self):
        v = getattr(self, field.name)
        url = '%d/%s/switch/' % (self._get_pk_val(), field.name)
        return '<a href ="%s" class="light_switch"><img src="/static/admin/img/icon-%s.svg" alt="%d" /></a>' % (
            url, ('no', 'yes')[v], v
        )

    _f.short_description = field.verbose_name
    _f.admin_order_field = field.name
    _f.allow_tags = True
    return _f


class LightAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    readonly_fields = ('created',)

    @property
    def media(self):
        m = super(LightAdmin, self).media
        return m + widgets.Media(js=('js/light_switch.js',))

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        list_display = []
        for field_name in self.list_display:
            try:
                db_field = self.model._meta.get_field(field_name)
                if isinstance(db_field, IntegerField):
                    field_name = light_switch_field(db_field)
            except FieldDoesNotExist:
                pass
            list_display.append(field_name)
        return list_display


admin.site.register(Light, LightAdmin)
