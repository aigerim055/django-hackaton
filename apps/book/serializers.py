from rest_framework import serializers
import logging
logger = logging.getLogger(__name__)

from .models import(
    Author,
    Book,
    Genre,
    BookImage
)


class BookListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(
        source='author.name'  
    )

    class Meta:
        model = Book
        fields = ['author', 'title', 'genre', 'image']


class BookSerializer(serializers.ModelSerializer):
    # logger.warning('WARNING')

    class Meta:
        model = Book
        fields = '__all__'

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError(
                'Price cannot be negative'
            )
        return price

    def validate_quantity(self, quantity):
        if quantity < 0:
            raise serializers.ValidationError('Quantity cannot be negative')
        return quantity

    def validate(self, attrs):
        title = attrs.get('title')
        if Book.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                'Such book already exists.'
            ) 
        return attrs
 
    def create(self, validated_data):                
        genre = validated_data.pop('genre')
        book = Book.objects.create(**validated_data)
        book.genre.set(genre)
        return book

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = BookImageSerializer(
            instance.book_images.all(),
            many=True
        ).data 
        return rep


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = 'image'


class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'slug']


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    books = BookListSerializer(read_only=True, many=True)   
    class Meta:
        model = Author
        fields = ['name', 'books']

    def to_representation(self, instance: Author):
        books = instance.books.all()
        representation = super().to_representation(instance)  
        representation['books'] = BookListSerializer(
            instance=books, many=True).data
        return representation


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('__all__')

    def validate(self, attrs):
        author = attrs.get('name')
        if Author.objects.filter(name=author).exists():
            raise serializers.ValidationError(
                'Such author already exists.'
            ) 
        return attrs


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

        def validate(self, attrs):
            genre = attrs.get('genre')
            if Genre.objects.filter(genre=genre).exists():
                raise serializers.ValidationError(
                    'Such genre already exists.'
                ) 
            return attrs


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre']


class GenreRetrieveSerializer(serializers.ModelSerializer):
    books = BookListSerializer(read_only=True, many=True)  
    class Meta:
        model = Genre
        fields = ['genre', 'books']

    def to_representation(self, instance: Genre):
        books = instance.books.all()
        representation = super().to_representation(instance)  
        representation['books'] = BookListSerializer(
            instance=books, many=True).data
        return representation