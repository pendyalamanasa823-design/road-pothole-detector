import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
from datetime import datetime

class PotholeDetector:
    """
    AI-powered pothole detection system using OpenCV
    """
    
    def __init__(self):
        self.min_area = 100
        self.max_area = 50000
        self.detections = []
    
    def detect_potholes(self, image_path, output_path=None):
        """
        Detect potholes in an image
        
        Args:
            image_path: Path to input image
            output_path: Path to save output image with bounding boxes
            
        Returns:
            dict: Detection results with confidence and bounding boxes
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {'success': False, 'error': 'Could not read image'}
            
            original_image = image.copy()
            height, width = image.shape[:2]
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
            
            # Apply morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            detections = []
            
            # Filter and process contours
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Check if contour area is within pothole range
                if self.min_area < area < self.max_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Calculate confidence based on area and shape
                    confidence = self._calculate_confidence(contour, area)
                    
                    if confidence > 0.5:  # Threshold for pothole detection
                        detections.append({
                            'x': int(x),
                            'y': int(y),
                            'width': int(w),
                            'height': int(h),
                            'area': int(area),
                            'confidence': round(confidence * 100, 2)
                        })
                        
                        # Draw bounding box on image
                        cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(original_image, f'{confidence*100:.1f}%', 
                                   (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Save output image if path provided
            if output_path:
                cv2.imwrite(output_path, original_image)
            
            return {
                'success': True,
                'total_potholes': len(detections),
                'detections': detections,
                'image_dimensions': {'width': width, 'height': height},
                'output_image': output_path
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _calculate_confidence(self, contour, area):
        """
        Calculate confidence score for pothole detection
        
        Args:
            contour: OpenCV contour
            area: Contour area
            
        Returns:
            float: Confidence score between 0 and 1
        """
        # Calculate circularity (how round the shape is)
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            return 0
        
        circularity = 4 * np.pi * area / (perimeter ** 2)
        
        # Potholes tend to be somewhat circular
        confidence = min(circularity, 1.0)
        
        return confidence
    
    def detect_video_potholes(self, video_path, output_path=None, sample_rate=5):
        """
        Detect potholes in video frames
        
        Args:
            video_path: Path to input video
            output_path: Path to save output video
            sample_rate: Process every nth frame
            
        Returns:
            dict: Detection results across frames
        """
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            all_detections = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every nth frame
                if frame_count % sample_rate == 0:
                    # Temporary save frame
                    temp_path = 'temp_frame.jpg'
                    cv2.imwrite(temp_path, frame)
                    
                    # Detect potholes in frame
                    result = self.detect_potholes(temp_path)
                    
                    if result['success']:
                        all_detections.append({
                            'frame': frame_count,
                            'detections': result['detections']
                        })
                    
                    # Clean up
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                
                frame_count += 1
            
            cap.release()
            
            return {
                'success': True,
                'total_frames': frame_count,
                'frames_processed': frame_count // sample_rate,
                'detections_by_frame': all_detections
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


def create_detector():
    """Factory function to create detector instance"""
    return PotholeDetector()
