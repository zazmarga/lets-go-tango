from importlib.metadata import requires
from random import choice

from django.contrib.auth.models import AbstractUser
from django.db import models

from lets_go_tango import settings


class Category(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(fields=["name", ],
                                    name="unique_category_name"
                                    ),
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


class Occupation(models.Model):
    name = models.CharField(max_length=63)
    description = models.CharField(max_length=155, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name", ],
                                    name="unique_occupation_name"
                                    ),
        ]

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=63)
    direction = models.CharField(max_length=155)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name



class Member(AbstractUser):
    occupations = models.ManyToManyField(Occupation, related_name="members")
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Activity(models.Model):
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]
    name = models.CharField(max_length=155)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    possessor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Place, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "activities"
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.name} ({self.location.name})"


class Opinion(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="opinions"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return self.content
