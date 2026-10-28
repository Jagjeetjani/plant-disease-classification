# 🌿 Project 6: Plant Disease Classification & Botanical Pathology

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-3.11-D00000?logo=keras&logoColor=white)](https://keras.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/Academic-AI%20Application%20Lab-059669)](https://www.cuchd.in/)

> **Chandigarh University** — Department of Computer Science & Engineering / Artificial Intelligence & Data Science  
> **Course:** AI Application Lab (Machine Learning & Deep Learning)  
> **Project Scope:** Project 6: Plant Disease Classification & Botanical Pathology

---

## 📌 1. Project Overview & Problem Formulation

Agricultural foliar diseases destroy 20% to 40% of global harvest yields annually, causing over **$220 Billion** in economic losses (FAO). In developing agricultural economies, smallholder farmers often lack access to professional plant pathologists, leading to delayed interventions or indiscriminate chemical pesticide spraying.

This project delivers an end-to-end, interpretable **Computer Vision Decision Support System** capable of identifying plant pathologies from leaf imagery in real time, explaining its reasoning using **Grad-CAM visual saliency heatmaps**, and issuing tailored **Integrated Pest Management (IPM)** prescriptions.

### Core Project Specifications
- **Problem Type:** Multi-Class Image Classification
- **Dataset:** Kaggle — PlantVillage (Multi-Crop Benchmark)
- **Objective:** Detect and classify foliar diseases from leaf photography
- **Input Features:** Leaf image pixels $(96 \times 96 \times 3 \text{ RGB})$
- **ML / DL Techniques:** Custom Deep Convolutional Neural Network (from scratch) and Transfer Learning (MobileNetV2 pre-trained on ImageNet)
- **Primary Metrics:** Accuracy, Precision, Recall, F1-Score, Inference Latency, Model Footprint
- **Explainable AI (XAI):** Gradient-weighted Class Activation Mapping (Grad-CAM)
- **Outcome:** Production-ready precision agriculture application for edge, mobile, and web

---

## 🌾 2. PlantVillage Pathology Taxonomy (15 Classes)

Our system monitors 15 distinct pathological and physiological states across 5 staple crops and orchard fruits:

| Host Crop | Botanical Condition | Scientific Pathogen | Etiology | Severity Level |
| :--- | :--- | :--- | :--- | :--- |
| **Tomato** | Early Blight | *Alternaria solani* | Fungus | High (Target-board rings) |
| **Tomato** | Late Blight | *Phytophthora infestans* | Oomycete | Critical (Water-soaked decay) |
| **Tomato** | Yellow Leaf Curl Virus | *TYLCV (Begomovirus)* | Virus | High (Severe chlorosis & curling) |
| **Tomato** | Healthy Foliage | *Pristine Plant State* | None | Normal / Vigorous |
| **Potato** | Early Blight | *Alternaria solani* | Fungus | Moderate to High |
| **Potato** | Late Blight | *Phytophthora infestans* | Oomycete | Devastating (Rapid foliage kill) |
| **Potato** | Healthy Foliage | *Pristine Plant State* | None | Normal / Vigorous |
| **Corn (Maize)** | Common Rust | *Puccinia sorghi* | Fungus | Moderate (Golden pustules) |
| **Corn (Maize)** | Northern Leaf Blight | *Exserohilum turcicum* | Fungus | High (Cigar-shaped lesions) |
| **Corn (Maize)** | Healthy Foliage | *Pristine Plant State* | None | Normal / Vigorous |
| **Apple** | Apple Scab | *Venturia inaequalis* | Fungus | High (Olive-black velvety spots) |
| **Apple** | Black Rot (Frog-Eye) | *Botryosphaeria obtusa* | Fungus | Moderate to Severe |
| **Apple** | Healthy Foliage | *Pristine Plant State* | None | Normal / Vigorous |
| **Bell Pepper** | Bacterial Spot | *Xanthomonas campestris* | Bacterium | High (Blistering angular spots) |
| **Bell Pepper** | Healthy Foliage | *Pristine Plant State* | None | Normal / Vigorous |

---

## 🏆 3. Quantitative Model Benchmarks & Comparison

Evaluated on 225 completely held-out test leaves across all 15 classes:

| Metric | Custom Deep CNN (Scratch) | Transfer Learning (MobileNetV2) | Winner / Champion |
| :--- | :--- | :--- | :--- |
| **Architecture** | 3-Block Conv2D + Dropout | Inverted Residuals + Linear Bottlenecks | — |
| **Pre-Trained Weights** | None (Random Xavier Init) | ImageNet (1.4M images) | **MobileNetV2** |
| **Test Accuracy** | **99.11%** | **100.00%** | 🏆 **MobileNetV2 (Champion)** |
| **Weighted Precision** | `0.9915` | **1.0000** | 🏆 **MobileNetV2** |
| **Weighted Recall** | `0.9911` | **1.0000** | 🏆 **MobileNetV2** |
| **Weighted F1-Score** | `0.9911` | **1.0000** | 🏆 **MobileNetV2** |
| **Inference Latency** | `15.2 ms / leaf (~65 FPS)` | `36.1 ms / leaf (~28 FPS)` | **Custom CNN** (Faster) |
| **Model Size on Disk** | `2.3 MB` | `9.8 MB` | **Custom CNN** (Smaller) |
| **Convergence** | 7 Epochs (24 sec) | 9 Epochs (54 sec) | **Both Rapid** |

---

## 🔬 4. Explainable AI (Grad-CAM) Visual Diagnostics

To provide trustworthy decisions for farmers, our system computes **Gradient-weighted Class Activation Mapping (Grad-CAM)**:

$$\alpha_k^c = \frac{1}{Z} \sum_i \sum_j \frac{\partial y^c}{\partial A_{i,j}^k}$$

$$L_{\text{Grad-CAM}}^c = \text{ReLU}\left( \sum_k \alpha_k^c A^k \right)$$

The resulting activation map superimposes a chromatic heatmap over the leaf:
- **Red / Warm Highlights:** Exact regions of highest neural attention (e.g., target rings of early blight, necrotic water-soaked margins, fungal pustules).
- **Blue / Cool Regions:** Background or healthy leaf lamina.

---

## 🖥️ 5. Interactive Streamlit Web Application

The application features 6 specialized agricultural modules:
1. 🌿 **AI Leaf Diagnosis (Scanner):** Supports 3 input sources (Preset 15-class benchmark gallery, custom photo upload, and live webcam snapshot). Displays real-time diagnosis, confidence bar, Top-3 probability distribution, Grad-CAM heatmaps, and agronomic prescriptions.
2. 📊 **Model Benchmarks & Metrics:** Side-by-side performance comparison, loss/accuracy curves, and confusion matrix heatmaps.
3. 🔬 **Exploratory Data Analysis (EDA):** RGB chlorophyll spectral distributions, HSV hue analysis, pathogen breakdown pie chart, and data augmentation pipeline.
4. 🧪 **Batch Diagnostic Lab:** Automated triage across multiple leaves with downloadable CSV reports.
5. 📚 **Agronomic Disease Encyclopedia:** Searchable compendium covering disease etiology, favorable climate triggers, chemical controls, and organic bio-remedies.
6. 👥 **Student & Course Profile:** University credentials, syllabus rubric alignments, and team attributions.

---

## 🚀 6. Quick Start Guide

### Option A: Windows 1-Click Launch (Recommended)
Simply double-click the included batch launcher:
```bat
run.bat
```
*The launcher automatically detects Python 3.10+, checks dependencies, verifies trained models, and starts the Streamlit web application at `http://localhost:8501` without closing.*

### Option B: Command Line (Windows / Linux / macOS)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch Streamlit Application
streamlit run app.py
```

### Option C: Re-Train Models & Regenerate Assets
```bash
# Generate sample leaves & database
python create_leaf_samples.py

# Create train/val/test dataset
python prepare_dataset.py

# Train Custom CNN & MobileNetV2
python model.py

# Generate EDA charts
python eda.py

# Compile 8-Page Academic PDF Report
python generate_report.py

# Compile 14-Slide 16:9 Presentation PPTX
python generate_ppt.py
```

---

## 📁 7. Repository Directory Structure

```
Plant Disease Classification/
│
├── .streamlit/
│   └── config.toml               # Agricultural Emerald custom theme
│
├── assets/
│   ├── cu_horizontal_logo.png    # Chandigarh University horizontal logo
│   └── cu_seal_logo.jpg          # University official seal
│
├── dataset/                      # 1,200 curated PlantVillage images
│   ├── train/                    # 750 training images across 15 classes
│   ├── val/                      # 225 validation images
│   └── test/                     # 225 held-out test images
│
├── models/
│   ├── custom_cnn_model.keras    # Saved Custom CNN model (2.3 MB)
│   ├── mobilenetv2_model.keras   # Saved MobileNetV2 model (9.8 MB)
│   ├── class_indices.json        # Class mapping dictionary
│   ├── disease_database.json     # Agronomic pathology & treatment knowledge base
│   └── model_metrics.json        # Empirical evaluation metrics & histories
│
├── sample_leaves/                # 15 high-res benchmark leaves for instant testing
│   ├── sample_apple___apple_scab.jpg
│   ├── sample_corn_(maize)___common_rust_.jpg
│   ├── sample_potato___late_blight.jpg
│   ├── sample_tomato___early_blight.jpg
│   └── ...
│
├── temp_charts/                  # High-resolution generated visual analytics
│   ├── augmentation_pipeline.png
│   ├── class_distribution.png
│   ├── confusion_matrix_cnn.png
│   ├── confusion_matrix_transfer.png
│   ├── disease_pathogen_breakdown.png
│   ├── hsv_color_space.png
│   ├── loss_accuracy_curves.png
│   ├── model_accuracy_comparison.png
│   └── rgb_color_distribution.png
│
├── app.py                        # Complete multi-page Streamlit web application
├── create_leaf_samples.py        # Botanical renderer & sample leaf creator
├── eda.py                        # Exploratory data analysis chart generator
├── generate_ppt.py               # 14-Slide widescreen PPTX generator
├── generate_report.py            # 8-Page academic lab report PDF generator
├── gradcam.py                    # Grad-CAM explainable AI saliency module
├── model.py                      # Deep learning training & evaluation script
├── prepare_dataset.py            # Dataset split creator
├── requirements.txt              # Project Python dependencies
├── run.bat                       # Windows launcher with persistent terminal
├── run.sh                        # Unix/macOS shell launcher
│
├── Plant_Disease_Classification_Report.pdf        # 8-page formatted academic lab report
└── Plant_Disease_Classification_Presentation.pptx  # 14-slide 16:9 widescreen presentation
```

---

## 🏛️ 8. Academic Laboratory Attribution

- **Course:** AI Application Lab (Machine Learning & Deep Learning)  
- **Department:** Department of Computer Science & Engineering / Artificial Intelligence & Data Science  
- **Institution:** Chandigarh University, Punjab, India  
- **Project Scope:** Project 6: Plant Disease Classification (PlantVillage Benchmark)
