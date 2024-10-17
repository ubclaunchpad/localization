from django.db import models
import uuid

# Create your models here.

class Token(models.Model):
    value = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)

class Translation(models.Model):
    token = models.foreignKey(Token, on_delete=models.CASCADE)
    original_word = models.charField(max_length = 255)
    translated_word = models.charField(max_length = 255)
    language = models.charField(max_length = 255)