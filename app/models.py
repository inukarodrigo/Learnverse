from django.db import models
from django.contrib.postgres.fields import JSONField


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def attributes(self):
        return self.__dict__

    class Meta:
        abstract = True


class Hit(BaseModel):
    data = JSONField(null=True)
