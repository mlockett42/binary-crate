# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from ..models import Project
from .serializers import ProjectGetSerializer, ProjectPostSerializer, DirectoryEntrySerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
#from .permissions import IsOwner
from project.models import DirectoryEntry
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
import copy


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class ProjectList(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        user = self.request.user
        #return Project.objects.none()
        return Project.objects.filter(owner=user)

    def get(self, request, format=None):
        projects = self.get_queryset()
        serializer = ProjectGetSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectPostSerializer(data=request.data)
        if serializer.is_valid():
            de = DirectoryEntry.objects.create(name='', is_file=False)
            serializer.save(owner=self.request.user, root_folder=de)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        if project.owner != request.user:
            raise PermissionDenied()
        serializer = ProjectGetSerializer(project)
        return Response(serializer.data)

class DirectoryEntryDetail(APIView):
    #permission_classes = (permissions.IsAuthenticated, )
    #authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self, pk):
        try:
            return DirectoryEntry.objects.get(pk=pk)
        except DirectoryEntry.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        #print('DirectoryEntryDetail request.data=', request.data)
        de = self.get_object(pk)
        serializer = DirectoryEntrySerializer(de, data=request.data)
        if serializer.is_valid():
            de = serializer.save()
            de.content = request.data['content'] # TODO: Add some validation here
            de.save()
            #print('DirectoryEntryDetail de=', de)
            response_data = copy.copy(serializer.data)
            response_data['content'] = de.content
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.save()
        #print('perform_update instance._content=', instance._content)


