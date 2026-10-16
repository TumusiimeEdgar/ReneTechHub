from django.db import models
from django.core.exceptions import ValidationError

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def clean(self):
        model_class = self.__class__
        if model_class.objects.exists() and not self.pk:
            raise ValidationError(
                f"You can only have one {model_class.__name__} entry. "
                "Please edit the existing record instead."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class About(SingletonModel):
    content_message = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    class Meta:
        verbose_name = "About"
        verbose_name_plural = "About"

    def __str__(self):
        return "Content"


class Education(models.Model):
    school_name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    year_month = models.DateField()
    description = models.TextField()

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['-year_month']

    def __str__(self):
        return self.school_name

    @property
    def year_display(self):
        return self.year_month.strftime("%B %Y")

from datetime import date
from django.db import models


class Work(models.Model):
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()

    class Meta:
        verbose_name = "Work"
        verbose_name_plural = "Work"
        ordering = ['-start_date']

    def __str__(self):
        return self.company_name

    @property
    def end_display(self):
        if self.end_date is None:
            return "Present"
        return self.end_date.strftime("%B %Y")

    @property
    def start_display(self):
        return self.start_date.strftime("%B %Y")


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    summery = models.CharField(max_length=100)
    project_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField()
    project_banner_image = models.ImageField(upload_to='project_banner_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Project"

    def __str__(self):
        return self.project_name


class Contact(SingletonModel):
    contact = models.CharField(max_length=13)
    email = models.EmailField()
    facebook_link = models.URLField()
    X_link = models.URLField()
    linked_in = models.URLField()
    address = models.TextField()

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contact"

    def __str__(self):
        return self.email


class SystemInfo(SingletonModel):
    system_name = models.CharField(max_length=100)
    system_short_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100, default="Your Name")
    welcome_message = models.TextField()
    system_logo = models.ImageField()
    background_image = models.ImageField(upload_to='background_images/', blank=True, null=True)

    class Meta:
        verbose_name = "System Info"
        verbose_name_plural = "System Info"

    def __str__(self):
        return self.system_name


class Testimonials(models.Model):
    client_name = models.CharField(max_length=100)
    testimony = models.TextField()
    background_image = models.ImageField(upload_to='background_images/', blank=True, null=True)

    class Meta:
        verbose_name = "Testimony"
        verbose_name_plural = "Testimony"

    def __str__(self):
        return self.client_name