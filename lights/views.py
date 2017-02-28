# -*- coding: utf-8 -*-
from django.apps import apps
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, ListView

from .models import Light


class LightListView(ListView):
    model = Light


class LightDetailView(DetailView):
    model = Light


def switch(request, url):
    """Switch status for Light objects."""
    statuses = {
        0: Light.OFF_STATUS,
        1: Light.ON_STATUS
    }
    admin, app_label, model_name, object_id, field = url.split('/')
    model = apps.get_model(app_label, model_name)
    object = get_object_or_404(model, pk=object_id)
    perm_str = '%s.change_%s' % (app_label, model.__name__)
    # check only model
    if not request.user.has_perm(perm_str.lower()):
        raise PermissionDenied

    next_value = 1
    current = getattr(object, field)
    if current == 1:
        next_value = 0

    setattr(object, field, next_value)
    object.save()

    if request.is_ajax():
        return JsonResponse({'object_id': object.pk, 'field': field, 'value': getattr(object, field)})
    else:
        msg = _(u'%(field)s was set to %(status) on %(object)s') % {'field': field,
                                                                    'status': statuses[next_value],
                                                                    'object': object}
        messages.success(request, msg)
        return HttpResponseRedirect(url)
