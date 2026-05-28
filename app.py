import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from detector import create_detector
import cv2
import base64

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mkv'}

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize detector
detector = create_detector()

# Store detection history
detection_history = []


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')


@app.route('/detect')
def detect_page():
    """Detection page"""
    return render_template('detect.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/api/detect', methods=['POST'])
def api_detect():
    """
    API endpoint for pothole detection
    Handles both image and video uploads
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Determine file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext in {'mp4', 'avi', 'mov', 'mkv'}:
            # Process video
            result = detector.detect_video_potholes(filepath)
        else:
            # Process image
            output_filename = f"output_{filename}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            result = detector.detect_potholes(filepath, output_path)
        
        if result['success']:
            # Add to detection history
            history_entry = {
                'timestamp': datetime.now().isoformat(),
                'filename': filename,
                'file_type': file_ext,
                'total_detections': result.get('total_potholes', 0),
                'detections': result.get('detections', [])
            }
            detection_history.append(history_entry)
            
            # Prepare response
            response = {
                'success': True,
                'total_potholes': result.get('total_potholes', 0),
                'detections': result.get('detections', []),
                'output_image': f"/static/outputs/output_{filename}" if 'output_image' in result else None,
                'timestamp': history_entry['timestamp']
            }
            
            return jsonify(response)
        else:
            return jsonify({'success': False, 'error': result.get('error', 'Detection failed')}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/detect-webcam', methods=['POST'])
def api_detect_webcam():
    """
    API endpoint for webcam frame detection
    """
    try:
        # Get base64 image data from request
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Save temporarily
        temp_path = 'temp_webcam.jpg'
        with open(temp_path, 'wb') as f:
            f.write(image_bytes)
        
        # Detect potholes
        output_path = 'temp_webcam_output.jpg'
        result = detector.detect_potholes(temp_path, output_path)
        
        if result['success']:
            # Read output image and encode to base64
            with open(output_path, 'rb') as f:
                output_image_data = base64.b64encode(f.read()).decode()
            
            response = {
                'success': True,
                'total_potholes': result['total_potholes'],
                'detections': result['detections'],
                'output_image': f"data:image/jpeg;base64,{output_image_data}"
            }
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(output_path):
                os.remove(output_path)
            
            return jsonify(response)
        else:
            return jsonify({'success': False, 'error': result.get('error')}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/history')
def api_history():
    """Get detection history"""
    return jsonify({
        'success': True,
        'total_detections': len(detection_history),
        'history': detection_history[-10:]  # Return last 10
    })


@app.route('/api/stats')
def api_stats():
    """Get statistics"""
    total_potholes = sum(entry['total_detections'] for entry in detection_history)
    total_uploads = len(detection_history)
    
    # Calculate severity (simplified)
    severity_high = sum(1 for entry in detection_history if entry['total_detections'] > 10)
    severity_medium = sum(1 for entry in detection_history if 5 < entry['total_detections'] <= 10)
    severity_low = sum(1 for entry in detection_history if 0 < entry['total_detections'] <= 5)
    
    return jsonify({
        'success': True,
        'total_potholes': total_potholes,
        'total_uploads': total_uploads,
        'average_potholes': total_potholes / total_uploads if total_uploads > 0 else 0,
        'severity': {
            'high': severity_high,
            'medium': severity_medium,
            'low': severity_low
        }
    })


@app.route('/api/download/<filename>')
def api_download(filename):
    """Download processed image"""
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
