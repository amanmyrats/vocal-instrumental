from django.db import models

class TestMp3(models.Model):
    name = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='audio/')
    
