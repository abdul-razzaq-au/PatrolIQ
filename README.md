# PatrolIQ - Smart Safety Analytics Platform
# 🚔 Crime Hotspot & Pattern Analysis Platform

## 📌 Project Overview

This project builds a **data-driven crime intelligence platform** using the Chicago Crime Dataset to identify **geographic hotspots, temporal crime patterns, and actionable policing strategies**.

The system leverages **unsupervised learning, dimensionality reduction, and interactive visualization** to support **smart patrol planning and public safety decision-making**.

---

## 🎯 Objectives

- Identify **geographic crime hotspots**
- Analyze **temporal crime patterns**
- Detect **high-risk zones and time periods**
- Provide **actionable patrol strategies**
- Build a **production-ready interactive dashboard**

---

## 🔄 Project Workflow

### **Step 1: Data Acquisition & Preprocessing**
- Downloaded Chicago Crime Dataset (**7.8M records, ~1.7GB**)
- Sampled **500,000 recent records** for analysis
- Performed:
  - Missing value handling
  - Data cleaning & validation
  - Datetime conversion
- Extracted temporal features:
  - Hour, Day of Week, Month

---

### **Step 2: Exploratory Data Analysis (EDA)**
- Analyzed distribution across **30+ crime types**
- Studied:
  - Geographic patterns (Latitude/Longitude)
  - Temporal trends (hourly, daily, seasonal)
- Examined:
  - Arrest rates
  - Domestic crime patterns
- Generated statistical summaries

---

### **Step 3: Feature Engineering**
- Created temporal features:
  - Hour, Day, Month, Weekend, Season
- Generated geographic features:
  - Coordinate binning
- Developed **Crime Severity Score**
- Applied:
  - Frequency encoding (Location Description)
- Normalized coordinates for clustering

---

## 🤖 Step 4: Clustering Analysis

### 📍 Geographic Clustering

#### **K-Means (Final Model)**
- Identified **7 distinct crime hotspots**
- Selected using:
  - Elbow Method
  - Silhouette Score

#### **DBSCAN**
- Detected **high-density crime areas**
- Identified **noise/outliers**
- Applied on sampled data for efficiency

#### **Hierarchical Clustering**
- Used Ward linkage
- Generated dendrograms to analyze cluster hierarchy

---

### ⏱️ Temporal Clustering

- Applied K-Means on:
  - Hour, Day, Month, Season
- Identified **5 temporal crime patterns**:
  - Late-night high-risk crimes
  - Weekend activity spikes
  - Seasonal patterns (Winter/Fall)
  - Daytime activity clusters

---

### 📊 Model Evaluation

- Silhouette Score
- Elbow Method
- Cluster consistency across methods

👉 **K-Means selected as final model** due to:
- Scalability
- Interpretability
- Consistent performance

---

## 📉 Step 5: Dimensionality Reduction

### **PCA (Principal Component Analysis)**
- First 2 components explained only **~38% variance**
- Required **~6 components for 70% variance**
- Indicated **high intrinsic dimensionality**

---

### **t-SNE**
- Captured **local cluster structures**
- Revealed non-linear patterns

---

### **UMAP (Best Technique)**
- Preserved **both local & global structure**
- Produced **clear cluster separation**
- Best visualization of crime patterns

---

### 🔥 Key Insight

> The dataset exhibits **complex non-linear relationships**, making PCA insufficient for low-dimensional representation.  
> Non-linear techniques like **UMAP provided the most meaningful visualization**.

---

## 📈 Step 7: MLflow Integration

- Integrated **MLflow + DagsHub**
- Tracked:
  - Clustering parameters (K, eps, etc.)
  - Model metrics (inertia, silhouette)
- Compared models and selected best
- Enabled experiment reproducibility

---

## 🌐 Step 8: Streamlit Application

Built an **interactive multi-page dashboard** with:

- 📍 Geographic crime maps (clusters + heatmaps)
- ⏱️ Temporal crime analysis dashboards
- 📊 PCA & UMAP visualizations
- 🧠 Cluster interpretation panels
- 🚔 Patrol strategy recommendations
- 📈 MLflow model monitoring

---

## ☁️ Step 9: Deployment

- Deployed on **Streamlit Cloud**
- Integrated with GitHub
- Ensured:
  - Responsive UI
  - Error handling
  - Smooth user experience

---

## 🧠 Key Insights

### 📍 Spatial Insights
- 7 crime hotspots identified:
  - Retail theft zones
  - Residential violence areas
  - Night-time high-risk zones

---

### ⏱️ Temporal Insights
- 5 patterns identified:
  - Late-night crime peaks
  - Weekend spikes
  - Seasonal variations
  - Daytime activity clusters

---

### 📊 Dimensionality Insights
- Data is **non-linear**
- UMAP > t-SNE > PCA for visualization

---

## 🚔 Patrol Strategy Recommendations

- 🔴 Increase patrol in **high-risk violent clusters**
- 🟠 Strengthen **night patrol deployment**
- 🔥 Deploy additional forces on **weekends**
- 🟡 Focus on **theft prevention in busy areas**
- ❄️ Adjust strategy for **seasonal crime trends**

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas, NumPy
- Scikit-learn
- Plotly
- UMAP
- MLflow + DagsHub

---
## Project structure
<pre>
├── streamlit_app.py
├── data/link_to_dataset.txt
├── Data_aquisition_and_sampling.ipynb
├── data_cleaning.ipynb
├── EDA_chicago_crime_data.ipynb
├── feature_engieering.ipynb
├── dimentionality_reduction.ipynb
├── requirements.txt
├── README.md
</pre>

MLFlow UI Link: https://dagshub.com/armaaz.au.stats/PatrolIQ.mlflow    <br>
App link : https://patroliq-8utkmekssatxpqcogtmcjp.streamlit.app/

---

