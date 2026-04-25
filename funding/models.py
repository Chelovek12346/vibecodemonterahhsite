from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=255)
    program = models.CharField(max_length=255)
    total_cost = models.FloatField()
    verified = models.BooleanField(default=False)
    trust_score = models.FloatField(default=0)


class FundingSource(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)  # grant, family, donation
    amount = models.FloatField()
    status = models.CharField(max_length=20, default="confirmed")
    metadata = models.JSONField(blank=True, null=True)


class Donation(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

