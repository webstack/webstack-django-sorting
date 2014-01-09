from django.db import models
from django.utils import timezone


class SecretFile(models.Model):
    filename = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    size = models.PositiveIntegerField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    is_secret = models.BooleanField()

    def __unicode__(self):
        return "#%d %s" % (self.pk, self.filename)
