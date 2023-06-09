from django.db import models

class Document(models.Model):
    pub = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    doc = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"{self.pub} - {self.chapter}"
