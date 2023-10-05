from django.db import models
from django.conf import settings

# Create your models here.
class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    videoID = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    content = models.TextField()

    TRAN = 'TRANSCRIPT'
    GEN = 'GENERATED'

    DOC_TYPES = (
        (TRAN, 'Transcript'),
        (GEN, 'AI Generated'),
    )

    type = models.CharField(max_length=150, choices=DOC_TYPES, default=TRAN)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

