from django.db import models

# Create your models here.

class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=100)
    message = models.TextField()