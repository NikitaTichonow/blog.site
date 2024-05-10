from rest_framework import serializers

from .import models

class FileModelSerializer(serializers.ModelSerializer):
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = models.PostFilesModel
        fields = ['title', 'file_path']

    @staticmethod
    def get_file_path(obj):
        return obj.file.path if obj.file else None

