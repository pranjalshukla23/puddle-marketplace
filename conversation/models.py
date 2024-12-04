from django.db import models
from items.models import Item
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    # many-to-one relationship - one item can belong to many conversation
    item = models.ForeignKey(Item, related_name="conversations", on_delete=models.CASCADE)
    # many-to-many relationship - a conversation can have multiple users, 
    # A single user can participate in multiple conversations.
    members = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-modified_at',)

class ConversationMessage(models.Model):
    # many-to-one relationship - one conversation can have many conversation messages
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # many-to-one relationship - one user can have many conversation messages
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)
    