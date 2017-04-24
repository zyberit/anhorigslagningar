from django.db import models

# Create your models here.

import datetime

class Case(models.Model):
    date = models.DateField(default=datetime.date.today)
    signatur = models.CharField("Signatur",default="NEW!!",db_index=True,max_length=5)
    objekt = models.CharField("Objekt",db_index=True,max_length=12)
    boss = models.CharField("Närmsta chef",max_length=5)
    action = models.IntegerField(default=-2)
    
    class Meta:
        ordering = ['signatur']
        verbose_name = "Fall"
        verbose_name_plural = "Fall"

    def __str__(self):
        return self.date.strftime("%Y%m%d")+":"+self.signatur+":"+self.objekt


class Slagningar(models.Model):
    timestamp = models.DateTimeField()
    system = models.CharField("System",max_length=10)
    signatur = models.CharField("Signatur",max_length=5)
    action = models.CharField("Signatur",max_length=10)
    objekt = models.CharField("Objekt",max_length=12)
    relation = models.CharField("Relation",max_length=30)
    info1 = models.CharField("Info 1",max_length=30)
    info2 = models.CharField("Info 2",max_length=30)
    info3 = models.CharField("Info 3",max_length=30)
    workplace = models.CharField("Anställdes arbetsort,",max_length=30)
    office = models.CharField("Af-kontor",max_length=30)
    boss = models.CharField("Närmsta chef",max_length=5)
    mo = models.CharField("Anställdes MO/Avd",max_length=30)
    moboss = models.CharField("MO/Avd-chef",max_length=5)
    case = models.ForeignKey(Case,db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Slagning"
        verbose_name_plural = "Slagningar"

    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")+":"+self.signatur+":"+self.objekt

