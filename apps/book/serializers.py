from rest_framework import serializers

from .models import(
    Author,
    Book,
    Genre
)


class BookListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(
        source='author.name'   # books.name?
    )

    class Meta:
        model = Book
        fields = ['author', 'title', 'genre', 'image']


# class CurrentAuthorDefault:
#     requires_context = True

#     def __call__(self, serializer_field):
#         return serializer_field.context['request'].author

#     def __repr__(self):
#         return '%s()' % self.__class__.__name__


class BookSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
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
        # user = self.context['request'].user   # надо ли? в нашем случае
        # attrs['user'] = user                  # надо ли? в нашем случае
        title = attrs.get('title')
        if Book.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                'Such book already exists.'
            ) 
        return attrs
 
    def create(self, validated_data):                       # надо ли
        genre = validated_data.pop('genre')
        book = Book.objects.create(**validated_data)
        book.genre.set(genre)
        return book


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