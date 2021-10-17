from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# class TargetManager(models.Manager):
#     def get_queryset(self):
#         return super(TargetManager, self).get_queryset().filter(status='in_progress')


class Task(models.Model):
    LEVEL_OF_DIFFICULTY = [
        ('hard', 'Hard'),
        ('medium', 'Medium'),
        ('easy', 'Easy'),
    ]
    STATUS_CHOICES = [
        ('start', 'Start'),
        ('in_progress', 'In progress'),
        ('finished', 'Finished'),
    ]

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='target_info')

    target = models.CharField(help_text="Jaki masz dzisiaj cel", max_length=100, null=False)
    slug = models.SlugField(max_length=100,
                            unique_for_date='created')

    created = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField(help_text="Od kiedy zaczynasz ?", null=False)
    end_date = models.DateTimeField(help_text="Do kiedy planujesz sończyć ?", null=False)
    updated = models.DateTimeField(auto_now=True)

    description = models.TextField(help_text="Informacje na temat zadania", max_length=300)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='S')
    difficulty_classification = models.CharField(help_text="Jak trudne może być to zadanie ? ",
                                                 max_length=10,
                                                 choices=LEVEL_OF_DIFFICULTY)
    # objects = models.Manager()
    # objects_target_manager = TargetManager()

    class Meta:
        ordering = ('-end_date',)

    def __str__(self):
        return self.target

    def get_absolute_url(self):
        return reverse('task_view:task_detail',
                       args=[self.created.year,
                             self.created.month,
                             self.created.day, self.slug])

