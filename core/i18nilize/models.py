from django.db import models
import uuid

# Create your models here.

class Token(models.Model):
    value = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)
