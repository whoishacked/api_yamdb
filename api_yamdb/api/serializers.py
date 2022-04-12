from rest_framework import serializers

from reviews.models import Titles, Category, Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug')
    genre = serializers.SlugRelatedField(slug_field='slug', many=True)

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
