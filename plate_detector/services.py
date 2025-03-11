import cv2
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
import os
from django.conf import settings
import pytesseract
from enum import Enum

class OCR_MODES(Enum):
    TRAINED = 'trained'
    TESSERACT = 'tesseract'

class PlateDetector:
    def __init__(self):
        # Initialize paths
        base_path = os.path.join(settings.BASE_DIR, 'weights')
        self.detection_weights = os.path.join(base_path, 'detection', 'yolov3-detection_final.weights')
        self.detection_cfg = os.path.join(base_path, 'detection', 'yolov3-detection.cfg')
        self.detection_classes = os.path.join(base_path, 'detection', 'classes-detection.names')
        
        # Load model
        self.net = cv2.dnn.readNetFromDarknet(self.detection_cfg, self.detection_weights)
        with open(self.detection_classes, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        self.layers_names = self.net.getLayerNames()
        unconnected_out_layers = self.net.getUnconnectedOutLayers().flatten()
        self.output_layers = [self.layers_names[i - 1] for i in unconnected_out_layers]
    
    def load_image(self, img_path):
        img = cv2.imread(img_path)
        height, width, channels = img.shape
        return img, height, width, channels

    def detect_plates(self, img):
        blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)
        return blob, outputs

    def get_boxes(self, outputs, width, height, threshold=0.3):
        boxes = []
        confidences = []
        class_ids = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > threshold:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        return boxes, confidences, class_ids

    def draw_labels(self, boxes, confidences, class_ids, img):
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
        font = cv2.FONT_HERSHEY_PLAIN
        plats = []
        max_confidence = 0
        
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                color_green = (0, 255, 0)
                crop_img = img[y:y + h, x:x + w]
                try:
                    crop_resized = cv2.resize(crop_img, dsize=(470, 110))
                    plats.append(crop_resized)
                    cv2.rectangle(img, (x, y), (x + w, y + h), color_green, 8)
                    confidence = round(confidences[i], 3) * 100
                    max_confidence = max(max_confidence, confidence)
                    # Adjust font scale and thickness
                    cv2.putText(img, str(confidence) + "%", (x + 20, y - 20), font, 2, (0, 255, 0), 2)
                except cv2.error:
                    pass

        return img, plats, max_confidence

class PlateReader:
    def __init__(self):
        # Initialize paths
        base_path = os.path.join(settings.BASE_DIR, 'weights')
        self.ocr_weights = os.path.join(base_path, 'ocr', 'yolov3-ocr_final.weights')
        self.ocr_cfg = os.path.join(base_path, 'ocr', 'yolov3-ocr.cfg')
        self.ocr_classes = os.path.join(base_path, 'ocr', 'classes-ocr.names')
        
        # Load model
        self.net = cv2.dnn.readNetFromDarknet(self.ocr_cfg, self.ocr_weights)
        with open(self.ocr_classes, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        
        self.layers_names = self.net.getLayerNames()
        unconnected_out_layers = self.net.getUnconnectedOutLayers().flatten()
        self.output_layers = [self.layers_names[i - 1] for i in unconnected_out_layers]
        
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
    
    def load_image(self, img_path):
        img = cv2.imread(img_path)
        height, width, channels = img.shape
        return img, height, width, channels

    def read_plate(self, img):
        blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.output_layers)
        return blob, outputs

    def get_boxes(self, outputs, width, height, threshold=0.3):
        boxes = []
        confidences = []
        class_ids = []
        for output in outputs:
            for detect in output:
                scores = detect[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > threshold:
                    center_x = int(detect[0] * width)
                    center_y = int(detect[1] * height)
                    w = int(detect[2] * width)
                    h = int(detect[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        return boxes, confidences, class_ids

    def draw_labels(self, boxes, confidences, class_ids, img):
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.1)
        font = cv2.FONT_HERSHEY_PLAIN
        c = 0
        characters = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                color = self.colors[i % len(self.colors)]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                confidence = round(confidences[i], 3) * 100
                cv2.putText(img, str(confidence) + "%", (x, y - 6), font, 1, color, 2)
                characters.append((label, x))
        characters.sort(key=lambda x: x[1])
        plate = ""
        for l in characters:
            plate += l[0]
        chg = 0
        for i in range(len(plate)):
            if plate[i] in ['b', 'h', 'd', 'a']:
                if plate[i - 1] == 'w':
                    ar = i - 1
                    chg = 2
                elif plate[i - 1] == 'c':
                    ar = i - 1
                    chg = 3
                else:
                    ar = i
                    chg = 1

        if chg == 1:
            plate = plate[:ar] + ' | ' + str(self.arabic_chars(ord(plate[ar])), encoding="utf-8") + ' | ' + plate[ar + 1:]
        if chg == 2:
            # Convert character to integer by summing ASCII values if needed
            index = sum(ord(plate[ar + j]) for j in range(3))
            plate = plate[:ar] + ' | ' + str(self.arabic_chars(index), encoding="utf-8") + ' | ' + plate[ar + 3:]
        if chg == 3:
            index = sum(ord(plate[ar + j]) for j in range(2))
            plate = plate[:ar] + ' | ' + str(self.arabic_chars(index), encoding="utf-8") + ' | ' + plate[ar + 2:]

        return img, plate

    def arabic_chars(self, index):
        if index == ord('a'):
            return "أ".encode("utf-8")
        if index == ord('b'):
            return "ب".encode("utf-8")
        if index == 2 * ord('w') + ord('a') or index == ord('w'):
            return "و".encode("utf-8")
        if index == ord('d'):
            return "د".encode("utf-8")
        if index == ord('h'):
            return "ه".encode("utf-8")
        if index == ord('c') + ord('h'):
            return "ش".encode("utf-8")

    def tesseract_ocr(self, image_path, lang="eng", psm=7):
        alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        options = f"-l {lang} --psm {psm} -c tessedit_char_whitelist={alphanumeric}"
        return pytesseract.image_to_string(image_path, config=options)

class PlateDetectionService:
    """Service for plate detection and OCR processing"""
    
    def __init__(self):
        self.detector = PlateDetector()
        self.reader = PlateReader()
    
    def process_image(self, image_path, ocr_mode=OCR_MODES.TRAINED):
        """
        Process an image to detect and read license plates
        
        Args:
            image_path: Path to the image file
            ocr_mode: OCR mode (TRAINED or TESSERACT)
            
        Returns:
            dict: Contains detection results including plate text and confidence
        """
        # Create temp directories if they don't exist
        tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)
        
        # Detect plate
        image, height, width, channels = self.detector.load_image(image_path)
        blob, outputs = self.detector.detect_plates(image)
        boxes, confidences, class_ids = self.detector.get_boxes(outputs, width, height, threshold=0.3)
        plate_img, LpImg, confidence = self.detector.draw_labels(boxes, confidences, class_ids, image)
        
        result = {
            'plate_text': None,
            'confidence': confidence,
            'detected_image_path': None,
            'plate_image_path': None
        }
        
        if not LpImg:
            return result
            
        # Save detected images
        car_box_path = os.path.join(tmp_dir, f"{os.path.basename(image_path)}_car_box.jpg")
        plate_box_path = os.path.join(tmp_dir, f"{os.path.basename(image_path)}_plate_box.jpg")
        
        cv2.imwrite(car_box_path, plate_img)
        cv2.imwrite(plate_box_path, LpImg[0])
        
        result['detected_image_path'] = car_box_path
        result['plate_image_path'] = plate_box_path
        
        # Apply OCR
        if ocr_mode == OCR_MODES.TRAINED:
            result['plate_text'] = self._apply_trained_ocr(plate_box_path)
        elif ocr_mode == OCR_MODES.TESSERACT:
            result['plate_text'] = self.reader.tesseract_ocr(plate_box_path)
            
        return result
    
    def _apply_trained_ocr(self, plate_path):
        """Apply trained OCR model to read the plate"""
        image, height, width, channels = self.reader.load_image(plate_path)
        blob, outputs = self.reader.read_plate(image)
        boxes, confidences, class_ids = self.reader.get_boxes(outputs, width, height, threshold=0.3)
        
        if not boxes:
            return None
            
        segmented, plate_text = self.reader.draw_labels(boxes, confidences, class_ids, image)
        
        # Save segmented image
        dirname = os.path.dirname(plate_path)
        segmented_path = os.path.join(dirname, f"{os.path.basename(plate_path)}_segmented.jpg")
        cv2.imwrite(segmented_path, segmented)
        
        return arabic_reshaper.reshape(plate_text)
