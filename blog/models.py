from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from phone_field import PhoneField
from django import forms 

# Create your models here.

class Post(models.Model):
    # sno = models.AutoField(primary_key=True, default=None)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})      


class JobApplication(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    phone = PhoneField(blank=True, help_text='Enter phone number')
    work_experience = models.TextField()
    resume = models.FileField(upload_to = 'resume', default='resume/default_resume.jpg')

    def __str__(self):
        return self.name
    