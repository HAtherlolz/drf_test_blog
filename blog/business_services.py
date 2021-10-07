import logging


from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response


from .models import *
from .serializer import PostsSerializer
from .service import PaginationPosts


logger = logging.getLogger(__name__)


def create_object(request, serializer_class):
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def _get_object(pk, model):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise Http404


def get_object_detail(request, pk, model, serializer_class):
    target_get = _get_object(pk, model)
    serializer = serializer_class(target_get)
    return Response(serializer.data)


def update_object(pk, request, model, serializer_class):
    target_update = _get_object(pk, model)
    serializer = serializer_class(target_update, data=request.data)
    if serializer.is_valid():
        if request.user == target_update.user:
            serializer.save()
            return Response(serializer.data)
        else:
            logger.info('Attempt to interact without authorization')
            return Response({"Permission Denied"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_object(request, pk, model):
    target_delete = _get_object(pk, model)
    if request.user == target_delete.user:
        target_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        logger.info('Attempt to interact without authorization')
        return Response({"Permission Denied"}, status=status.HTTP_400_BAD_REQUEST)
