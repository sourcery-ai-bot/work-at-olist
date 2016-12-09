"""Models of the Channels app."""

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class BaseModel(models.Model):
    """BaseModel is an abstract model with: UUID primary key field and Unique
    reference field.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(_('Reference'), max_length=100, unique=True)

    class Meta:
        """BaseModel Meta options."""
        abstract = True


class Channel(BaseModel):
    """Channel represents places where products can be published."""

    name = models.CharField(_('Name'), max_length=256, unique=True)

    class Meta:
        """Channel Meta options."""

        ordering = ['reference']
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    def __str__(self):
        return self.reference


class Category(MPTTModel, BaseModel):
    """Category represents products's hierarquical organization on a Channel."""

    name = models.CharField(_('Name'), max_length=256)
    channel = models.ForeignKey(
        Channel, related_name='categories', verbose_name=_('Channel'))
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        """Category Meta options."""
        ordering = ['channel', 'reference']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    class MPTTMeta:
        """Category MPTTMeta options."""
        order_insertion_by = ['reference']

    def __str__(self):
        return self.reference
