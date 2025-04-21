from django.db import models # type: ignore

# Create your models here.

class Add_mission(models.Model):
    theme = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    img_mission = models.ImageField(upload_to='images_mission/', null=True, blank=True)
    lien = models.URLField(null=True, blank=True)
    description = models.TextField()

    def imgmission_url(self):
        if self.img_mission:
            return self.img_mission.url
        return "media/images_mission/"
    
    
class Add_pubfb(models.Model):
    theme_fb = models.CharField(max_length=100)
    date_fb = models.DateTimeField(auto_now_add=True)
    img_fb = models.ImageField(upload_to='images_fb/', null=True, blank=True)
    lien_fb = models.URLField(null=True, blank=True)
    description_fb = models.TextField()

    def imgfb_url(self):
        if self.img_fb:
            return self.img_fb.url
        return "media/images_fb/"

class Add_admin(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    img = models.ImageField(upload_to='images_admin/', null=True, blank=True)
    password = models.CharField(max_length=100)

    def imgadmin_url(self):
        if self.img:
            return self.img.url
        return "media/images_admin/"