from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

TASK_STATUS_CHOICE = (
    ('Pending', 'Pending'),
    ('Finished', 'Finished'),
    ('InReview', 'InReview'),
    ('Debugging', 'Debugging'),
    ('Finished After Debugging', 'Finished After Debugging'),
)
STATUS = (
    ('InReview', 'InReview'),
)


class Stage(models.Model):
    entry = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return "%s" % (self.entry)


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=10)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, )
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, )
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='stage1', related_query_name='stage1_q',
                              blank=True)

    def __str__(self):
        return self.title

    class Meta:
        pass


class Process(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    title = models.CharField(max_length=10)
    priority = models.PositiveIntegerField(validators=[MinValueValidator(1)], unique=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='process',
                                related_query_name='process_q')

    def __str__(self):
        return "%s: %s" % (self.project.title, self.title)

    class Meta:
        ordering = ['-priority']


class Task(models.Model):
    user_createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_assignedto = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='task_assignedto')
    title = models.CharField(max_length=15, )
    image = models.FileField(upload_to=None, null=True, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=30, choices=TASK_STATUS_CHOICE, null=True)
    order = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=False, unique=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='task', related_query_name='task_q')

    def __str__(self):
        return "%s: %s" % (self.process.title, self.title)

    class Meta:
        ordering = ['-order']


class Status(models.Model):
    status = models.CharField(max_length=30, choices=STATUS)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='status1', related_query_name='status_q1',
                                unique=True)

    def __str__(self):
        return "%s" % (self.status)
