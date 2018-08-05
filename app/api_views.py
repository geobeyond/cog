from .models import COG
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


class COG_APIView(APIView):
    parser_class = (FileUploadParser,)

    def get(self, request, format=None):
        cogs = [cog.name for cog in COG.objects.all()]
        return Response(cogs)

    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']

        COG.image.save(f.name, f, save=True)
        return Response(status=status.HTTP_201_CREATED)
        

    def put(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']

        COG.image.save(f.name, f, save=True)
        return Response(status=status.HTTP_201_CREATED)
