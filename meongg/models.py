from django.db import models

# Create your models here.


class Hackathon(models.Model):
    idx = models.AutoField(primary_key=True)
    data_time = models.DateTimeField()
    data_value = models.IntegerField()
    data_type = models.CharField(max_length=45)
    data_from = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'hackathon'