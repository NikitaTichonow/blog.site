from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers


class GetFilePath(APIView):
    @staticmethod
    def get(request):
        code = request.GET.get('code')
        try:
            file = models.PostFilesModel.objects.get(code=code)
            file.increment_download_count()
            serialized_data = serializers.FileModelSerializer(file)
            return Response(serialized_data.data)
        except ObjectDoesNotExist:
            return Response(None, status=404)


class CreateBotUser(APIView):
    @staticmethod
    def post(request):
        usr_obj: models.BotUserModel = models.BotUserModel.objects.get_or_create(
            chat_id=request.data['chat_id'],
            defaults={
                'first_name': request.data['first_name'],
                'last_name': request.data['last_name'],
                'username': request.data['username'],
            })[0]
        usr_obj.save()
        return Response(status=200)