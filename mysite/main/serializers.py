from rest_framework import serializers
from .models import Articles, Comments

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'author', 'content']
    

class ArticlesSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Articles
        fields = ['id', 'title', 'summary', 'full_text', 'date', 'comments']
