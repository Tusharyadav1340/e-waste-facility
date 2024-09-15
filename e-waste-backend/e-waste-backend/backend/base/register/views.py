# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EventCard, EventRegistration, CastImage
from base.models import CustomUser
from .serializers import EventCardSerializer, EventRegistrationSerializer, CastImageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from base.models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class EventCardView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = EventCardSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()

            cast_images_data = request.data.getlist('cast_images', [])
            for cast_image_data in cast_images_data:
                CastImage.objects.create(event=event, image=cast_image_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # print(request.headers)
        id = request.query_params.get('id')
        if id:
            event = get_object_or_404(EventCard, id=id)
            serializer = EventCardSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        events = EventCard.objects.all().order_by('-date')
        serializer = EventCardSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from rest_framework.decorators import api_view, permission_classes, authentication_classes

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_event(request):
        print(request.headers)
        id = request.query_params.get('id')
        if id:
            event = get_object_or_404(EventCard, id=id)
            serializer = EventCardSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        events = EventCard.objects.all().order_by('-date')
        serializer = EventCardSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def register(request):
    try:
        user = request.user
        mutable_data = request.data.copy()
        mutable_data['user'] = user.id
        serializer = EventRegistrationSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EventRegistrationView(APIView):
            
    def get(self, request):
        event_id = request.GET.get('event_id')
        try:
            if event_id:
                event = EventRegistration.objects.filter(event_id=event_id)
                serializer = EventRegistrationSerializer(event, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Event registration not found"})
        except EventRegistration.DoesNotExist:
            return Response({"error": "Event registration not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddCastImageView(APIView):
    def post(self, request, event_id, format=None):
        try:
            event = EventCard.objects.get(id=event_id)
        except EventCard.DoesNotExist:
            return Response({'error': 'EventCard not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CastImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
