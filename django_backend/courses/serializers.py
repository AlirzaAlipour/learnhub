from rest_framework import serializers
from .models import Course, Chapter

class CourseSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['instructor', 'title', 'description']
        read_only_fields = ['instructor']


class ChapterSerializer (serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['course', 'chapter_number', 'video_file', 'photo_file', 'pdf_file']
        read_only_fields = ['course']



