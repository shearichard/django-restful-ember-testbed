from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import AllowAny 
from rosebiology.serializers import UserSerializer, GroupSerializer

from .models import Species, Rose, CommonName  
from .serializers import SpeciesSerializer, RoseSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#################################################################################

class SpeciesList(APIView):
    """
    List all code species, or create a new species.
    """
    permission_classes = (AllowAny,)
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    def get(self, request, format=None):
        species = Species.objects.all()
        serializer = SpeciesSerializer(species, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SpeciesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpeciesDetail(APIView):
    """
    Retrieve, update or delete a code species.
    """
    permission_classes = (AllowAny,)
    def get_object(self, pk):
        try:
            return Species.objects.get(pk=pk)
        except Species.DoesNotExist:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        species = self.get_object(pk)
        serializer = SpeciesSerializer(species)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        species = self.get_object(pk)
        serializer = SpeciesSerializer(species, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_NOT_FOUND)

    def delete(self, request, pk, format=None):
        species = self.get_object(pk)
        species.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#################################################################################
#################################################################################

class RoseList(APIView):
    """
    List all rose, or create a new rose.
    """
    permission_classes = (AllowAny,)
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    def get(self, request, format=None):
        rose = Rose.objects.all()
        serializer = RoseSerializer(rose, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RoseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoseDetail(APIView):
    """
    Retrieve, update or delete a code rose.
    """
    permission_classes = (AllowAny,)
    def get_object(self, pk):
        try:
            return Rose.objects.get(pk=pk)
        except Rose.DoesNotExist:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        rose = self.get_object(pk)
        serializer = RoseSerializer(rose)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        rose = self.get_object(pk)
        serializer = RoseSerializer(rose, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_NOT_FOUND)

    def delete(self, request, pk, format=None):
        rose = self.get_object(pk)
        rose.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#################################################################################
