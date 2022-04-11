from rest_framework import serializers

from titles.models import Titles, Category, Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre
