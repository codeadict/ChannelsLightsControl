import json

from channels import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, AutoSlugField


class Light(TimeStampedModel):
    """Database model representing a light bulb."""
    OFF_STATUS, ON_STATUS = range(2)
    STATUS_CHOICES = (
        (OFF_STATUS, _('Off')),
        (ON_STATUS, _('On')),
    )
    name = models.CharField(_('Name'), max_length=255)
    slug = AutoSlugField(_('Slug'), populate_from='name')
    status = models.IntegerField(_('Status'), choices=STATUS_CHOICES, default=OFF_STATUS)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def send_status_update(self):
        """
        Sends a status updates to subscribed channels.
        """
        command = {
            "light_id": self.id,
            "status": self.status,
            "created": self.created.strftime("%a %d %b %Y %H:%M"),
        }
        Group('lights').send({
            # WebSocket text frame, with JSON content
            "text": json.dumps(command),
        })

    def save(self, *args, **kwargs):
        """
        Hooking send_notification into the save of the object as I'm not
        the biggest fan of signals.
        """
        result = super().save(*args, **kwargs)
        self.send_status_update()
        return result
