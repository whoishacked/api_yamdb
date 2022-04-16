from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Genre serializer."""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class TitlePostPatchSerializer(serializers.ModelSerializer):
    """Title patch & post serializer."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = datetime.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def get_rating(self, obj):
        if obj.reviews.all():
            rating = obj.reviews.aggregate(Avg('score'))
            return int(rating.get('score__avg'))
        return None


class TitleSerializer(serializers.ModelSerializer):
    """Title serializer."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        if obj.reviews.all():
            rating = obj.reviews.aggregate(Avg('score'))
            return int(rating.get('score__avg'))
        return None


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserRegSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
