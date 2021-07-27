from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='users/profile_pics', default='users/profile_pics/default.jpg')

    def __str__(self):
        return f'{self.user} Profile'

    # If saving images locally, use this to resize images to save space
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # run parent class' save() method when we save instance of profile

        img = Image.open(self.profile_pic.path)  # open image of current instance

        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)  # override the large image
