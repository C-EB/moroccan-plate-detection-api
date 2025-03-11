from django.db import models
import uuid
import os

def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads/', filename)

class PlateDetection(models.Model):
    """Model for storing plate detection results"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_path)
    result_image = models.ImageField(upload_to='results/', blank=True, null=True)
    plate_text = models.CharField(max_length=50, blank=True, null=True)
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    OCR_CHOICES = (
        ('trained', 'Trained Model'),
        ('tesseract', 'Tesseract OCR'),
    )
    ocr_method = models.CharField(max_length=10, choices=OCR_CHOICES, default='trained')
    
    def __str__(self):
        return f"{self.plate_text or 'Unknown'} - {self.id}"