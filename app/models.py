from django.db import models

class snacks(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class store(models.Model):
    storename=models.CharField(max_length=100)
    snacks=models.ManyToManyField(snacks)
    qty=models.IntegerField()
    rate=models.IntegerField()
    
    
    
    def __str__(self):
        return self.stroename
    
