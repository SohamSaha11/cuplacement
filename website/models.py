from django.db import models

# Create your models here.

class users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    isPlacementCell = models.BooleanField()


class companies(models.Model):
    companyName = models.CharField(max_length=50)
    description = models.TextField()
    branchesEligible = models.CharField(max_length=500)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    stipendOffer = models.IntegerField()
    additionalBenefits = models.TextField()
    registerLink = models.URLField(max_length=200)
    deadline = models.DateTimeField()
    publishDate = models.DateTimeField()
    girlsOnly = models.BooleanField()


class notices(models.Model):
    compName = models.CharField(max_length=50)
    notice = models.TextField()
    expiryDate = models.DateTimeField()
    pubDate = models.DateTimeField()


class placedrecord(models.Model):
    rollNumber = models.IntegerField()
    name = models.CharField(max_length=30)
    email = models.EmailField()
    year = models.IntegerField()
    companyName = models.CharField(max_length=50)
    accept = models.BooleanField()


class reviews(models.Model):
    user_id = models.IntegerField()
    user_email = models.EmailField()
    review = models.TextField()
    publishDate = models.DateTimeField()
    companyID = models.IntegerField()