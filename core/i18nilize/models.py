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
    microservice_token = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    project_token = models.ForeignKey(Token, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Microservice Token: {str(self.microservice_token)} - Project Token: {str(self.project_token)}"

class Writer(models.Model):
    project_token = models.ForeignKey(Token, on_delete=models.CASCADE)
    editor_token = models.ForeignKey(MicroserviceToken, null=True, on_delete=models.SET_NULL, related_name="write_permissions")

    def __str__(self):
        return f"Project: {self.project_token} - Editor: {self.editor_token or 'None'}"