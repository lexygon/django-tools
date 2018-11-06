from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Yaratılma Tarihi"))
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Güncelleme Tarihi"))
    deleted_at = models.DateTimeField(editable=False, verbose_name=_("Silinme Tarihi"), blank=True, null=True)

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(TimeStampedModel, self).delete()
