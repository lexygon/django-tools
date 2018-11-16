from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_tools.managers import SoftDeletionManager, StatusableManager


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Yaratılma Tarihi"))
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Güncelleme Tarihi"))
    deleted_at = models.DateTimeField(editable=False, verbose_name=_("Silinme Tarihi"), blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(TimeStampedModel, self).delete()


class StatusAwareModel(models.Model):
    ACTIVE = 'active'
    PASSIVE = 'passive'
    STATUSES = ()

    _STATUSES = (
        (ACTIVE, _('Aktif')),
        (PASSIVE, _('Pasif'))
    ) + STATUSES

    status = models.CharField(max_length=30, verbose_name=_('Durum'), blank=True, default=ACTIVE, choices=_STATUSES)

    objects = StatusableManager()
    all_objects = StatusableManager(awake_only=False)

    class Meta:
        abstract = True

    def active(self):
        self.status = self.ACTIVE
        self.save()

    def passive(self):
        self.status = self.PASSIVE
        self.save()
