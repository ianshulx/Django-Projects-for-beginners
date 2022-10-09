# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.
class Books(models.Model):
    book_id = models.CharField(max_length=10, blank=False, primary_key=True)    
    title = models.CharField(max_length=200, blank=False)
    author = models.ForeignKey('Author')
    isbn = models.BigIntegerField(blank=False)
    publisher = models.ForeignKey('Publisher')
    due_date = models.DateField(blank=True, null=True, default=None)
    issue_date = models.DateField(blank=True, null=True, default=None)
    return_date = models.DateField(blank=True, null=True, default=None)
    request_issue = models.BooleanField(default=False)
    issue_status = models.BooleanField(default=False)
    fine = models.IntegerField(default=0)
    email = models.EmailField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.book_id + " - " + self.title

    def __unicode__(self):
        return self.book_id + " - " + self.title

    class Meta:
        ordering = ['title']

class Author(models.Model):
    firstname = models.CharField(max_length=200, blank=False)
    lastname = models.CharField(max_length=200, blank=False)
    dob = models.DateField(blank=False)
    fullname = models.CharField(max_length=200, blank=False, null=False)
    def __str__(self):
        return self.firstname + " " + self.lastname

    def __unicode__(self):
        return self.firstname + " " + self.lastname

    class Meta:
        ordering = ['lastname']

class Publisher(models.Model):
    name = models.CharField(max_length=200, blank=False)
    country = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name + " " + self.country

    def __unicode__(self):
        return self.name + " " + self.country

    class Meta:
        ordering = ['name']

class Student(models.Model):
    male = 'Male'
    female = 'Female'
    it = 'IT'
    ece = 'ECE'

    GENDER_CHOICES = (
        (male, 'Male'),
        (female, 'Female'),
    )

    BRANCH_CHOICES = (
        (it, 'IT'),
        (ece, 'ECE'),
    )

    SEMESTER_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    department = models.CharField(max_length=100, choices=BRANCH_CHOICES)
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    fullname = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.user.username + " " + self.enrollment_no

    def __unicode__(self):
        return self.user.username + " " + self.enrollment_no

    class Meta:
        ordering = ['semester']

class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    librarian_id = models.CharField(max_length=20, blank=False)
    fullname = models.CharField(max_length=100, blank=False, null=False)
    def __str__(self):
        return self.user.username + " " + self.librarian_id

    def __unicode__(self):
        return self.user.username + " " + self.librarian_id

    class Meta:
        ordering = ['first_name']

class Issue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book = models.OneToOneField(Books, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.book.book_id

    def __unicode__(self):
        return self.user.username + ' ' + self.book.book_id
    