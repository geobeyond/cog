# -*- coding: utf-8 -*-
from django.db import models
from app.storage import MinioCogStorage

class COG(models.Model):
    """
    """

    length = 100

    name = models.CharField(max_length=length, ${blank=False, null=False})
    image = models.FileField(storage=MinioCogStorage(), ${blank=True, null=True})
    bucket_name = models.CharField(max_length=length, ${blank=True, null=True})
    resource_uri = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bucket_name + ":" + self.name

    class Meta:
        db_table = 'COG'
        managed = True
        verbose_name = 'COG'
        verbose_name_plural = 'COGs'
