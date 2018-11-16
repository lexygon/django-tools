from django.db import models
from django.utils import timezone


class StatusableQuerySet(models.QuerySet):
    def delete(self):
        return super(StatusableQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(StatusableQuerySet, self).delete()

    def awake(self):
        return self.filter(status=self.model.ACTIVE)

    def sleeping(self):
        return self.exclude(status=self.model.PASSIVE)

    def active(self):
        return super(StatusableQuerySet, self).update(status=self.model.ACTIVE)

    def passive(self):
        return super(StatusableQuerySet, self).update(status=self.model.PASSIVE)


class StatusableManager(models.Manager):
    _queryset_class = StatusableQuerySet

    def __init__(self, *args, **kwargs):
        self.awake_only = kwargs.pop('awake_only', True)
        super(StatusableManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        qs = self._queryset_class(self.model, using=self.db, hints=self._hints)

        if self.awake_only:
            return qs.filter(status=self.model.ACTIVE)
        return qs


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    _queryset_class = SoftDeletionQuerySet

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        qs = self._queryset_class(self.model, using=self.db, hints=self._hints)

        if self.alive_only:
            return qs.filter(deleted_at=None)
        return qs

    def hard_delete(self):
        return self.get_queryset().hard_delete()
