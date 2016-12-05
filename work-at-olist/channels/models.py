"""
Models of the Channels app.
"""

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

class BaseModel(models.Model):
    """
    BaseModel is an abstract model with:
        - UUID primary key field;
        - Unique reference field;
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(_('Reference'), max_length=100, unique=True)

    class Meta:
        abstract = True
