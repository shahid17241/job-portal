from django.db import models
from django.conf import settings

# Create your models here.
class Job(models.Model):
    title  = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_applied = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job', 'applicant'],
                name='unique_job_application',
            ),
        ]

    def __str__(self):
        return f"{self.applicant} applied to {self.job}"
