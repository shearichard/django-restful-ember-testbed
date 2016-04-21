from rest_framework import serializers

from django.contrib.auth.models import User, Group

from .models import Species, Rose


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('binomial_nomenclature', 'subspecies', 'common_name', 'height_and_spread', 'range', 'use', 'further_reference', 'image', 'created', 'modified')

class RoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rose 
        fields = ('binomial_nomenclature', 'height_and_spread', 'created', 'modified')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
