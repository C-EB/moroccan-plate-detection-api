from rest_framework import serializers
from .models import PlateDetection

class PlateDetectionSerializer(serializers.ModelSerializer):
    """Serializer for plate detection model"""
    class Meta:
        model = PlateDetection
        fields = ['id', 'image', 'result_image', 'plate_text', 'confidence', 'created_at', 'ocr_method']
        read_only_fields = ['id', 'result_image', 'plate_text', 'confidence', 'created_at']

class PlateDetectionResultSerializer(serializers.ModelSerializer):
    """Serializer for returning detection results"""
    class Meta:
        model = PlateDetection
        fields = ['id', 'image', 'result_image', 'plate_text', 'confidence', 'created_at', 'ocr_method']
