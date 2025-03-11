from django.contrib import admin
from .models import PlateDetection

@admin.register(PlateDetection)
class PlateDetectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'plate_text', 'confidence', 'created_at', 'ocr_method']
    list_filter = ['ocr_method', 'created_at']
    search_fields = ['plate_text', 'id']
    readonly_fields = ['id', 'created_at']