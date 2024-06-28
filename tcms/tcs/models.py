
from django.contrib.auth.models import User
from django.db import models

    
class Project(models.Model):
    # Define attributes for File table as per your requirementscl
    project_name = models.CharField(max_length=255,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.project_name


# File Model (assuming basic attributes for now)
class File(models.Model):
    # Define attributes for File table as per your requirements
    file_name = models.CharField(max_length=255,primary_key=True)
    file_path = models.CharField(max_length=1024)
    project_name=models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.file_name   

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')

    def __str__(self):
        return self.user.username

class TCS(models.Model):
    testcase_id = models.AutoField(primary_key=True)
    testcase_name = models.CharField(max_length=255)
    testcase_result = models.CharField(max_length=10)
    testcase_type = models.CharField(max_length=100)
    testcase_description = models.TextField(blank=True, null=True)
    file_name= models.ForeignKey(File, on_delete=models.CASCADE)
    testcase_group = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.testcase_name} - {self.testcase_type} - {self.testcase_result} - {self.testcase_group}"
