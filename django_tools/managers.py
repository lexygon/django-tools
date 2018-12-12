from django.db import models
from django.utils import timezone


class StatusableQuerySetMixin(object):
    def awake(self):
        return self.filter(status=self.model.ACTIVE)

    def sleeping(self):
        return self.exclude(status=self.model.PASSIVE)

    def active(self):
        return super(StatusableQuerySetMixin, self).update(status=self.model.ACTIVE)

    def passive(self):
        return super(StatusableQuerySetMixin, self).update(status=self.model.PASSIVE)


class StatusableQuerySet(StatusableQuerySetMixin, models.QuerySet):
    pass


class StatusableManagerMixin(object):
    awake_only = True

    def get_queryset(self):
        qs = super(StatusableManagerMixin, self).get_queryset()

        if self.awake_only:
            return qs.filter(status=self.model.ACTIVE)
        return qs


class StatusableManager(StatusableManagerMixin, models.Manager):
    _queryset_class = StatusableQuerySet

    def __init__(self, *args, **kwargs):
        self.awake_only = kwargs.pop('awake_only', True)
        super(StatusableManager, self).__init__(*args, **kwargs)


class SoftDeletionQuerySetMixin(object):
    def delete(self):
        return super(SoftDeletionQuerySetMixin, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySetMixin, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionQuerySet(SoftDeletionQuerySetMixin, models.QuerySet):
    pass


class SoftDeletionManagerMixin(object):
    alive_only = True

    def get_queryset(self):
        qs = super(SoftDeletionManagerMixin, self).get_queryset()

        if self.alive_only:
            return qs.filter(deleted_at=None)
        return qs

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionManager(SoftDeletionManagerMixin, models.Manager):
    _queryset_class = SoftDeletionQuerySet

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)
