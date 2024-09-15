# serializers.py
from rest_framework import serializers
from django.core.files.base import ContentFile
import base64
import six
import uuid
from .models import EventCard, EventRegistration, CastImage

class LowercaseEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        return data.lower()

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")
        return super(Base64ImageField, self).to_internal_value(data)

class CastImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastImage
        fields = ['id', 'image']

class EventCardSerializer(serializers.ModelSerializer):
    img = Base64ImageField(max_length=None, use_url=True)
    cast_images = CastImageSerializer(many=True, read_only=True)

    class Meta:
        model = EventCard
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cast_images = representation.get('cast_images', [])
        
        # Assign custom IDs starting from 1 for each event's cast images
        for index, cast_image in enumerate(cast_images, start=1):
            cast_image['id'] = index

        return representation

class EventRegistrationSerializer(serializers.ModelSerializer):
    email = LowercaseEmailField()

    class Meta:
        model = EventRegistration
        fields = '__all__'

class GetEventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = EventRegistration
        fields = '__all__'
