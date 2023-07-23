from django.db import models
from django.utils.translation import gettext_lazy as _


class Sponsor(models.Model):
    class SponsorType(models.TextChoices):
        PHYSICAL = "physical", _('Physical person')
        JURIDICAL = "juridical", _("Legal entity")

    class Status(models.TextChoices):
        NEW = 'new', _("New")
        MODERATION = 'moderation', _("IN Moderation")
        CONFIRMED = "confirmed", _("Confirmed")
        CANCELED = "canceled", _("Canceled")

    sponsor_type = models.CharField(
        max_length=15, choices=SponsorType.choices, default=SponsorType.PHYSICAL
    )
    fullname = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    money = models.BigIntegerField(default=0)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.MODERATION
    )
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")
        ordering = ['-created_at']


class University(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _("Universities")


class Student(models.Model):
    class StudentType(models.TextChoices):
        BACHELOR = "bachelor", _("Bachelor")
        MASTER = "master", _("Master")

    fullname = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, related_name="student", null=True
    )
    student_type = models.CharField(
        max_length=15, choices=StudentType.choices, default=StudentType.BACHELOR
    )
    contract = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name_plural = _("Students")
        ordering = ['-created_at']


class Sponsorship(models.Model):
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.CASCADE, related_name="sponsorship"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="sponsorship"
    )
    money = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sponsor} - {self.student}: {self.money} so'm"

    class Meta:
        verbose_name_plural = _("Sponsorships")
        ordering = ['-created_at']
        unique_together = ('sponsor', 'student')
