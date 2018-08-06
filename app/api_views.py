from .models import COG
from PIL import Image
import rasterio
from django.shortcuts import get_object_or_404
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
        cogs = [{
            "id": cog.id,
            "name": cog.name,
            "bucket_name": cog.bucket_name,
            "resource_uri": cog.resource_uri,
            "created_at": cog.created_at,
            "updated_at": cog.updated_at
        } for cog in COG.objects.all()]
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

        f_name = COG.objects.filter(name=name)
        if f_name.count() > 0:
            return Response(status=status.HTTP_409_CONFLICT)

        # try to open file with rasterio
        try:
            with rasterio.open(img) as dataset:
                data_array = dataset.read() 
        except:
            raise ParseError("Unsupported image type opened by Rasterio") 

        cog = COG.objects.create(name=name, image=img)
        cog.save()
        return Response(status=status.HTTP_201_CREATED)


class COGDetailView(APIView):
    """
    This view should return the Cloud Optimized Geotiff queryset
    as determined by the uuid portion of the URL.
    """
    parser_class = (ImageUploadParser,)

    def get_queryset(self):
        uuid = self.kwargs['uuid']
        return COG.objects.filter(id=uuid)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        # self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, format=None, *args, **kwargs):
        cog_item = self.get_object()
        cog = {
            "id": cog_item.id,
            "name": cog_item.name,
            "bucket_name": cog_item.bucket_name,
            "resource_uri": cog_item.resource_uri,
            "created_at": cog_item.created_at,
            "updated_at": cog_item.updated_at
        }
        return Response(cog)
        

    def put(self, request, format=None, *args, **kwargs):
        """

        Example
        -------
        Example of request for creating a COG resource.
        
            $   curl -X PUT \
                http://localhost:5000/api/cogs/<id> \
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

        cog_item = self.get_object()
        cog = COG.objects.filter(
            id=cog_item.id
        ).update(name=name, image=img)
        cog.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, format=None, *args, **kwargs):
        """
        """

        cog_item = self.get_object()
        cog = COG.objects.filter(
            id=cog_item.id
        )
        cog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
