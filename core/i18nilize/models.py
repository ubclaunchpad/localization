from django.db import models
import uuid

# Create your models here.

class Token(models.Model):
    value = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)

class Translation(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    original_word = models.CharField(max_length = 255)
    translated_word = models.CharField(max_length = 255)
    language = models.CharField(max_length = 255)

class MicroserviceToken(models.Model):
    value = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    project_token = models.ForeignKey(Token, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)

class Writer(models.Model):
    project_token = models.ForeignKey(Token, on_delete=models.CASCADE, null=False, blank=False)
    editor_token = models.ForeignKey(MicroserviceToken, null=True, on_delete=models.SET_NULL, related_name="write_permissions")

    # Ensures that a project token (and editor token) can only appear once in writer
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['project_token'], name='unique_project_token'),
            models.UniqueConstraint(fields=['editor_token'], name='unique_editor_token')
        ]

    def __str__(self):
        return f"Project: {self.project_token} - Editor: {self.editor_token or 'None'}"