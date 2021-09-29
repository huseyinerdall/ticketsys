from rest_framework import serializers
from app.models import Ticket, User, Category, Attachment, Comment

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'category', 'assignee', 'type', 'subject', 'status', 'detail',\
                  'labels', 'attachments','comments', 'owner', 'severity')
        model = Ticket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name', 'department', 'bio', 'password', 'profile_image')
        model = User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'description')
        model = Category

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'file')
        model = Attachment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user', 'comment', 'created_at')
        model = Comment