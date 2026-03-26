from django.db import models


class Image(models.Model):
    file = models.ImageField(upload_to='uploads/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = models.JSONField(default=list)
    description = models.TextField(blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.filename
