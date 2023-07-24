from rest_framework import serializers
from classifier.models import wordsListModel

class wordsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = wordsListModel
        fields = ('text', )