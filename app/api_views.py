from .models import COG
from cog.settings.development import RASTERIO_COGEO_PROFILE
from PIL import Image
import rasterio
import os
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles
from rasterio.io import MemoryFile
from django.shortcuts import get_object_or_404
from django.core.files import File
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

        # try to open file with rasterio and validate cog
        # see https://pythonexample.com/code/validate%20cloud%20optimized%20geotiff/
        # PR to exploit when merged
        # https://github.com/mapbox/rio-cogeo/pull/6
        with rasterio.open(img) as dataset:
            is_cog = True
            try:
                assert dataset.driver == "GTiff"
                assert dataset.is_tiled
                assert dataset.overviews(1)
            except (
                AttributeError,
                KeyError
            ):
                raise ParseError(
                    "Unsupported image type opened by Rasterio"
                )
            except AssertionError:
                # @TODO add logging if it isn't COG
                is_cog = False

            inpt_profile = dataset.profile
            block_size = 512
            config = dict(
                NUM_THREADS=8,
                GDAL_TIFF_INTERNAL_MASK=os.environ.get("GDAL_TIFF_INTERNAL_MASK", True),
                GDAL_TIFF_OVR_BLOCKSIZE=os.environ.get("GDAL_TIFF_OVR_BLOCKSIZE", block_size),
            )
            if not is_cog:
                cog_img_name = "cog" + "_" + name
                cog_profile = cog_profiles.get(RASTERIO_COGEO_PROFILE)
                cog_profile.update(dict(BIGTIFF=os.environ.get("BIGTIFF", "IF_SAFER")))
                with MemoryFile(filename=cog_img_name) as dst:
                    with dst.open(**inpt_profile) as cog_img:
                        cog_translate(
                            dataset.files[0],
                            cog_img.files[0],
                            cog_profile,
                            indexes=None,
                            nodata=None,
                            alpha=None,
                            overview_level=6,
                            config=config
                        )
                    dst.seek(0)
                    ci_file = File(dst)
                    ci_file.name = os.path.basename(ci_file.name)
                    cog = COG.objects.create(name=ci_file.name, image=ci_file)

        if not cog_img:
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
        # see https://github.com/mapbox/rio-glui/blob/master/rio_glui/raster.py
        with rasterio.open(img) as dataset:
            is_cog = True
            try:
                assert dataset.driver == "GTiff"
                assert dataset.is_tiled
                assert dataset.overviews(1)
            except (
                AttributeError,
                AssertionError,
                KeyError
            ) as err:
                if err[0] or err[2]:
                    raise ParseError(
                        "Unsupported image type opened by Rasterio"
                    )
                elif err[1]:
                    # @TODO add logging if it isn't COG
                    is_cog = False
            data_array = dataset.read()
        
        if not is_cog:
            pass

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
