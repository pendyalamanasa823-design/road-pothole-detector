# 🚗 AI-Powered Road Pothole Detection Website

A modern, futuristic web application that detects potholes in road images and videos using computer vision and deep learning techniques.

## 🌟 Features

- **Modern UI/UX**: Glassmorphism design with dark theme and smooth animations
- **Image & Video Upload**: Support for multiple file formats
- **Real-time Detection**: AI-powered pothole detection using OpenCV
- **Live Webcam Detection**: Stream detection from your webcam
- **Dashboard Analytics**: Track detection statistics and history
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop
- **Download Results**: Export processed images with bounding boxes
- **Detection Confidence**: View confidence percentages for detections

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask
- **Computer Vision**: OpenCV
- **Image Processing**: NumPy, Pillow
- **Deployment**: GitHub Ready

## 📁 Project Structure

```
road-pothole-detector/
├── static/
│   ├── css/
│   │   ├── styles.css
│   │   ├── detection.css
│   │   ├── dashboard.css
│   │   └── about.css
│   ├── js/
│   │   ├── main.js
│   │   ├── detection.js
│   │   ├── dashboard.js
│   │   └── utils.js
│   ├── uploads/
│   ├── outputs/
│   └── images/
├── templates/
│   ├── index.html
│   ├── detect.html
│   ├── dashboard.html
│   └── about.html
├── app.py
├── detector.py
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Modern web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/pendyalamanasa823-design/road-pothole-detector.git
cd road-pothole-detector
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

## 📖 Pages Overview

### Home Page
- Hero section with animated background
- Project description
- Features showcase
- Quick start button
- Responsive navigation

### Detection Page
- File upload (image/video)
- Live webcam capture
- Real-time preview
- Detection processing
- Result visualization with bounding boxes
- Confidence metrics
- Download functionality

### Dashboard
- Total detections count
- Detection statistics
- Recent uploads history
- Severity indicators
- Interactive charts

### About Page
- Problem statement
- How it works
- Technologies explained
- Team information

## 🔍 Detection Algorithm

The pothole detection system uses:
1. **Grayscale conversion** - Simplifies image processing
2. **Gaussian blur** - Reduces noise
3. **Edge detection** - Identifies boundaries
4. **Contour analysis** - Finds pothole regions
5. **Bounding boxes** - Highlights detected potholes
6. **Confidence scoring** - Rates detection accuracy

## 🎨 Design Features

- Glassmorphism cards with transparency effects
- Dark futuristic theme with gradients
- Smooth CSS animations and transitions
- Particle background animation
- Loading spinners
- Hover effects on interactive elements
- Custom scrollbar styling
- Mobile-first responsive design

## 📱 Browser Support

- Chrome/Edge (Latest)
- Firefox (Latest)
- Safari (Latest)
- Mobile browsers

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created for portfolio and demonstration purposes.

---

**Note**: For best results, use high-quality road images with clear pothole visibility. The system works best with daylight photos.
