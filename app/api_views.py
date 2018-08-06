from .models import COG
from PIL import Image
import rasterio
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ImageUploadParser(FileUploadParser):
    media_type = 'image/*'


class COGListCreateView(APIView):
    parser_class = (ImageUploadParser,)

    def get(self, request, format=None):
        cogs = [{"name": cog.name} for cog in COG.objects.all()]
        return Response(cogs)
        

    def post(self, request, format=None):
        """

        Example
        -------
        Example of request for creating a COG resource.
        
            $   curl -X POST \
                http://localhost:5000/api/cogs/ \
                -u 'cog:cog' \
                -H 'Content-Disposition: attachment; filename=example.tif' \
                -H 'Content-Type: image/tif' \
                -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
                -F image=@/Users/geobart/example.tif \
                -F name=example.tif
        """
        
        if 'image' not in request.data.keys():
            raise ParseError("Empty content")
        
        img = request.data['image']
        name = request.data['name']

        # try to open file with rasterio
        try:
            with rasterio.open(img) as dataset:
                data_array = dataset.read() 
        except:
            raise ParseError("Unsupported image type opened by Rasterio") 

        cog = COG.objects.create(name=name, image=img)
        cog.save()
        return Response(status=status.HTTP_201_CREATED)
    
    # def delete(self, request, format=None):
    #     COG.delete(save=True)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
