from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PlateDetection
from .serializers import PlateDetectionSerializer, PlateDetectionResultSerializer
from .services import PlateDetectionService, OCR_MODES
from django.conf import settings
import os
from django.core.files.base import ContentFile
import cv2

class PlateDetectionViewSet(viewsets.ModelViewSet):
    """ViewSet for plate detection operations"""
    queryset = PlateDetection.objects.all()
    serializer_class = PlateDetectionSerializer
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return PlateDetectionResultSerializer
        return PlateDetectionSerializer
    
    def create(self, request, *args, **kwargs):
        """Handle image upload and perform plate detection"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save instance
        instance = serializer.save()
        
        # Process the uploaded image
        ocr_method = instance.ocr_method
        ocr_mode = OCR_MODES.TRAINED if ocr_method == 'trained' else OCR_MODES.TESSERACT
        
        service = PlateDetectionService()
        result = service.process_image(instance.image.path, ocr_mode)
        
        # Update instance with detection results
        if result['detected_image_path']:
            with open(result['detected_image_path'], 'rb') as f:
                instance.result_image.save(
                    os.path.basename(result['detected_image_path']), 
                    ContentFile(f.read()), 
                    save=False
                )
        
        instance.plate_text = result['plate_text']
        instance.confidence = result['confidence']
        instance.save()
        
        # Return updated serialized data
        return Response(
            PlateDetectionResultSerializer(instance).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'])
    def detect_bulk(self, request):
        """Detect plates in multiple images at once"""
        if 'images' not in request.FILES:
            return Response(
                {'error': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ocr_method = request.data.get('ocr_method', 'trained')
        results = []
        
        for image_file in request.FILES.getlist('images'):
            # Create a PlateDetection instance
            instance = PlateDetection(
                image=image_file,
                ocr_method=ocr_method
            )
            instance.save()
            
            # Process the image
            ocr_mode = OCR_MODES.TRAINED if ocr_method == 'trained' else OCR_MODES.TESSERACT
            service = PlateDetectionService()
            result = service.process_image(instance.image.path, ocr_mode)
            
            # Update instance with detection results
            if result['detected_image_path']:
                with open(result['detected_image_path'], 'rb') as f:
                    instance.result_image.save(
                        os.path.basename(result['detected_image_path']), 
                        ContentFile(f.read()), 
                        save=False
                    )
            
            instance.plate_text = result['plate_text']
            instance.confidence = result['confidence']
            instance.save()
            
            results.append(PlateDetectionResultSerializer(instance).data)
        
        return Response(results, status=status.HTTP_201_CREATED)
