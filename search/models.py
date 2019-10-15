from django.db import models

# Create your models here.

class DataSet(models.Model):
    name = models.CharField(max_length=255)
    value = models.BigIntegerField()

    class Meta:
        db_table = 'tbl_data_set'
