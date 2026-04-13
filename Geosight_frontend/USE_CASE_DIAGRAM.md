# GeoSight Frontend - Use Case Diagram

```
                                    GEOSIGHT SYSTEM
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                          ┌──────────────────────────────┐                      │
│                          │   Browse Landing Page        │                      │
│         ┌────────────────│   - View Hero Section        │                      │
│         │                │   - See Trust Indicators     │                      │
│         │                │   - Learn How It Works       │                      │
│         │                │   - View Architecture Flow   │                      │
│         │                │   - See Use Cases & Impact   │                      │
│         │                └──────────────────────────────┘                      │
│         │                                                                       │
│         │                ┌──────────────────────────────┐                      │
│         │                │   Upload & Classify Image    │◄─────────┐           │
│         │    ┌───────────│   - Upload Satellite Image   │          │           │
│         │    │           │   - Drag & Drop File         │          │           │
│         │    │           │   - View Processing Status   │          │           │
│         │    │           │   - Get AI Predictions       │          │           │
│         │    │           │   - View Confidence Scores   │          │           │
│         │    │           │   - See Class Distribution   │          │           │
│         │    │           │   - View 4-Panel Viz         │          │           │
│         │    │           └──────────────────────────────┘          │           │
│         │    │                                                     │           │
│         │    │           ┌──────────────────────────────┐          │           │
│    ┌────┴────┴───┐       │   Map-Based Analysis         │          │           │
│    │             │   ┌───│   - Search by Place Name     │          │           │
│    │   General   │   │   │   - Get Current Location     │          │           │
│    │    User     │───┤   │   - Enter Manual Coordinates │          │           │
│    │  (Visitor)  │   │   │   - Navigate Map             │          │           │
│    │             │   │   │   - Draw Rectangle on Map    │          │           │
│    └─────────────┘   │   │   - Select Analysis Model    │          │           │
│                      │   │     * Land Classification    │          │           │
│                      │   │     * Road Detection         │          │           │
│                      │   │   - Fetch Satellite Image    │          │           │
│                      │   │   - Run AI Analysis          │          │           │
│                      │   │   - View Results             │          │           │
│                      │   └──────────────────────────────┘          │           │
│                      │                                             │           │
│                      │   ┌──────────────────────────────┐          │           │
│                      │   │   View Model Insights        │          │           │
│                      └───│   - Switch Between Models    │          │           │
│                          │     * Land Classification    │          │           │
│                          │     * Road Detection         │          │           │
│                          │   - View Model Summary       │          │           │
│                          │   - See Performance Radar    │          │           │
│                          │   - Analyze Class Performance│          │           │
│                          │   - View Confusion Matrix    │          │           │
│                          │   - See Training Graphs      │          │           │
│                          │   - Check Feature Importance │          │           │
│                          │   - Use Prediction Simulator │          │           │
│                          └──────────────────────────────┘          │           │
│                                                                     │           │
│                          ┌──────────────────────────────┐          │           │
│                          │   Explore Interactive Map    │          │           │
│                          │   - View Classified Regions  │          │           │
│                          │   - See Location Markers     │          │           │
│                          │   - View Popup Details       │          │           │
│                          │   - Navigate India Map       │          │           │
│                          └──────────────────────────────┘          │           │
│                                                                     │           │
│                          ┌──────────────────────────────┐          │           │
│                          │   Learn About Project        │          │           │
│                          │   - View Project Overview    │          │           │
│                          │   - See Objectives           │          │           │
│                          │   - Learn Data Sources       │          │           │
│                          │   - View Preprocessing Steps │          │           │
│                          │   - See Model Training Info  │          │           │
│                          │   - Check Model Evaluation   │          │           │
│                          │   - View Suitability Analysis│          │           │
│                          │   - See Project Timeline     │          │           │
│                          │   - View Workflow Diagram    │          │           │
│                          │   - Check Tech Stack         │          │           │
│                          │   - See Factory Suitability  │          │           │
│                          │   - View Impact Metrics      │          │           │
│                          └──────────────────────────────┘          │           │
│                                                                     │           │
│                          ┌──────────────────────────────┐          │           │
│                          │   View Team Information      │          │           │
│                          │   - See Team Members         │          │           │
│                          │   - View Roles               │          │           │
│                          │   - Read Responsibilities    │          │           │
│                          └──────────────────────────────┘          │           │
│                                                                     │           │
│                                                                     │           │
│                          ┌──────────────────────────────┐          │           │
│                          │   Backend API Integration    │◄─────────┘           │
│                          │   (External System)          │                      │
│                          │   - Fetch Satellite Images   │                      │
│                          │   - Run Land Classification  │                      │
│                          │   - Run Road Detection       │                      │
│                          │   - Generate Visualizations  │                      │
│                          │   - Return Predictions       │                      │
│                          └──────────────────────────────┘                      │
│                                                                                 │
│                          ┌──────────────────────────────┐                      │
│                          │   Google Earth Engine        │                      │
│                          │   (External System)          │                      │
│                          │   - Provide Sentinel-2 Data  │                      │
│                          │   - Process Satellite Imagery│                      │
│                          └──────────────────────────────┘                      │
│                                                                                 │
│                          ┌──────────────────────────────┐                      │
│                          │   OpenStreetMap / Nominatim  │                      │
│                          │   (External System)          │                      │
│                          │   - Provide Map Tiles        │                      │
│                          │   - Geocoding Services       │                      │
│                          │   - Place Name Search        │                      │
│                          └──────────────────────────────┘                      │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════

                            KEY FEATURES & INTERACTIONS

═══════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  PRIMARY USE CASES:                                                             │
│  ═════════════════                                                              │
│                                                                                 │
│  1. IMAGE UPLOAD & CLASSIFICATION                                              │
│     • User uploads satellite image (JPG/PNG/TIFF)                              │
│     • System processes with U-Net++ model                                      │
│     • Returns: Dominant class, confidence, class distribution                  │
│     • Displays: 4-panel visualization (original, segmented, overlay, chart)    │
│                                                                                 │
│  2. MAP-BASED ANALYSIS                                                         │
│     • User searches place by name OR enters coordinates OR draws on map        │
│     • System fetches Sentinel-2 imagery from Google Earth Engine               │
│     • User selects model: Land Classification OR Road Detection                │
│     • System runs selected AI model                                            │
│     • Returns: Predictions with visualizations                                 │
│                                                                                 │
│  3. LAND CLASSIFICATION                                                        │
│     • 4-class segmentation: Background, Rural, Urban, Water                    │
│     • Model: U-Net++ with EfficientNet-B4 backbone                             │
│     • Input: 6-channel Sentinel-2 imagery (256x256 tiles)                      │
│     • Output: Class percentages, confidence scores, pixel counts               │
│                                                                                 │
│  4. ROAD DETECTION                                                             │
│     • Binary segmentation for road network extraction                          │
│     • Model: U-Net with ResNet-50 encoder                                      │
│     • Input: 3-channel RGB imagery (256x256 tiles)                             │
│     • Output: Road coverage %, road pixels, total pixels                       │
│                                                                                 │
│  5. MODEL PERFORMANCE INSIGHTS                                                 │
│     • Switch between Classification & Road Detection models                    │
│     • View comprehensive metrics and analytics                                 │
│     • Interactive charts and visualizations                                    │
│     • Expandable cards for detailed exploration                                │
│                                                                                 │
│  6. EDUCATIONAL CONTENT                                                        │
│     • Complete project documentation                                           │
│     • Technical architecture details                                           │
│     • Data pipeline explanation                                                │
│     • Team information                                                         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════

                            TECHNICAL ARCHITECTURE

═══════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  FRONTEND STACK:                                                                │
│  • React 18 + Vite (Fast development & HMR)                                     │
│  • React Router DOM (Client-side routing)                                       │
│  • Framer Motion (Smooth animations & transitions)                              │
│  • Tailwind CSS (Utility-first styling)                                         │
│  • Three.js + React Three Fiber (3D visualizations)                             │
│  • Leaflet + Leaflet Draw (Interactive maps & drawing)                          │
│  • GSAP (Advanced animations)                                                   │
│                                                                                 │
│  PAGES:                                                                         │
│  1. Home (/)           - Landing page with hero, features, use cases            │
│  2. Live Demo (/demo)  - Upload & map-based analysis interface                  │
│  3. Insights (/insights) - Model performance metrics & analytics                │
│  4. Map (/map)         - Interactive classified regions map                     │
│  5. About (/about)     - Project documentation & technical details              │
│  6. Team (/team)       - Team members & responsibilities                        │
│                                                                                 │
│  KEY COMPONENTS:                                                                │
│  • MapUploadPanel - Dual-mode upload (file/map) with model selection            │
│  • EnhancedPredictionCard - Results display with metrics                        │
│  • FourPanelVisualization - Multi-view image analysis                           │
│  • RoadVisualization - Road detection results display                           │
│  • ConfusionMatrix - Model performance visualization                            │
│  • TrainingGraph - Training metrics over epochs                                 │
│  • PerformanceRadar - Multi-metric radar chart                                  │
│                                                                                 │
│  BACKEND INTEGRATION:                                                           │
│  • REST API: http://localhost:5000                                              │
│  • Endpoints:                                                                   │
│    - POST /api/fetch-image (Land classification)                                │
│    - POST /api/detect-roads (Road detection)                                    │
│    - GET /api/download/{filename} (Visualization download)                      │
│                                                                                 │
│  EXTERNAL SERVICES:                                                             │
│  • Google Earth Engine - Sentinel-2 satellite imagery                           │
│  • OpenStreetMap - Map tiles & base layers                                      │
│  • Nominatim - Geocoding & place name search                                    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════

                            USER WORKFLOWS

═══════════════════════════════════════════════════════════════════════════════════

WORKFLOW 1: File Upload Classification
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 1. User navigates to Live Demo page                                            │
│ 2. User selects "Upload Image" mode                                            │
│ 3. User drags & drops or browses for satellite image file                      │
│ 4. User clicks "Run Classification"                                            │
│ 5. System displays processing overlay                                          │
│ 6. System returns prediction results                                           │
│ 7. User views enhanced prediction card with metrics                            │
│ 8. User clicks to view 4-panel visualization                                   │
│ 9. User sees: Original | Segmented | Overlay | Distribution Chart              │
└─────────────────────────────────────────────────────────────────────────────────┘

WORKFLOW 2: Map-Based Land Classification
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 1. User navigates to Live Demo page                                            │
│ 2. User selects "Select from Map" mode                                         │
│ 3. User selects "Land Classification" model                                    │
│ 4. User searches place name (e.g., "Delhi") OR enters coordinates              │
│ 5. Map navigates to location                                                   │
│ 6. User draws rectangle on desired area using draw tool                        │
│ 7. System displays selected bounds coordinates                                 │
│ 8. User clicks "Analyze with AI Model"                                         │
│ 9. System fetches Sentinel-2 imagery from Google Earth Engine                  │
│ 10. System runs U-Net++ classification model                                   │
│ 11. System returns: Dominant class, class distribution, confidence scores      │
│ 12. User views results and 4-panel visualization                               │
└─────────────────────────────────────────────────────────────────────────────────┘

WORKFLOW 3: Map-Based Road Detection
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 1. User navigates to Live Demo page                                            │
│ 2. User selects "Select from Map" mode                                         │
│ 3. User selects "Road Detection" model                                         │
│ 4. User searches place OR enters coordinates OR draws on map                   │
│ 5. User clicks "Analyze with AI Model"                                         │
│ 6. System fetches satellite imagery                                            │
│ 7. System runs U-Net road detection model                                      │
│ 8. System returns: Road coverage %, road pixels, total pixels                  │
│ 9. User views road detection visualization                                     │
│ 10. User sees extracted road network overlay                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

WORKFLOW 4: Explore Model Performance
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 1. User navigates to Model Insights page                                       │
│ 2. User switches between "Land Classification" and "Road Detection" models     │
│ 3. User clicks on expandable cards to view detailed metrics:                   │
│    • Model Summary (architecture, parameters, training details)                │
│    • Performance Radar (multi-metric visualization)                            │
│    • Class Performance (per-class IoU, precision, recall)                      │
│    • Confusion Matrix (classification accuracy breakdown)                      │
│    • Training Graph (loss & accuracy curves over epochs)                       │
│    • Feature Importance (band contribution analysis)                           │
│    • Prediction Simulator (interactive testing)                                │
│ 4. User closes expanded card to return to overview                             │
└─────────────────────────────────────────────────────────────────────────────────┘

WORKFLOW 5: Learn About Project
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 1. User navigates to About page                                                │
│ 2. User clicks on expandable cards to explore:                                 │
│    • Project Overview (goals, models, statistics)                              │
│    • Objective (4-class segmentation + road detection)                         │
│    • Data Sources (Sentinel-2, Google Earth Engine)                            │
│    • Data Preprocessing (tiling, normalization, augmentation)                  │
│    • Model Training (architecture, hyperparameters, optimization)              │
│    • Model Evaluation (metrics, validation results)                            │
│    • Suitability Analysis (industrial site selection use case)                 │
│    • Project Timeline (development phases)                                     │
│    • Workflow Diagram (end-to-end pipeline)                                    │
│    • Tech Stack (frameworks, libraries, tools)                                 │
│    • Factory Suitability (real-world application)                              │
│    • Impact Metrics (project outcomes)                                         │
│ 3. User closes expanded card to continue exploring                             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Summary

**GeoSight Frontend** is a comprehensive web application that provides:

1. **Dual Analysis Modes**: File upload and interactive map-based analysis
2. **Two AI Models**: Land classification (4-class) and road detection (binary)
3. **Rich Visualizations**: 4-panel views, confusion matrices, training graphs, radar charts
4. **Interactive Maps**: Leaflet-powered with drawing tools and geocoding
5. **Educational Content**: Complete project documentation and team information
6. **Modern UX**: Smooth animations, responsive design, intuitive workflows

**Target Users**: Researchers, urban planners, GIS analysts, students, and anyone interested in geospatial AI applications.

**Core Value**: Makes complex satellite imagery analysis accessible through an intuitive, visually engaging interface.
