from django.db import models
from accounts.models import User

class Course (models.Model):
    instructor = models.ForeignKey(User, related_name="courses", on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField()
    published = models.BooleanField(default=False)

class Chapter (models.Model):
    course = models.ForeignKey(Course, related_name="chapters", on_delete=models.CASCADE)
    chapter_number = models.PositiveIntegerField(unique=True)
    video_file = models.FileField(blank=True, null=True)
    photo_file = models.ImageField(blank=True, null=True)
    pdf_file = models.FileField(blank=True, null=True)
    published = models.BooleanField(default=False)