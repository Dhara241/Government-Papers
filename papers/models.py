from django.db import models

class Exam(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. GPSC, GSSSB")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
