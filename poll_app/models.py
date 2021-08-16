from django.db import models
from django.core.exceptions import ValidationError


# Poll model
class Poll(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError("EndDate less then StartDate")
