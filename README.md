# AI for Sustainable Cities – SDG 11

## 🎯 Interactive Presentation

**🎭 [View the Interactive Presentation](https://plp-academy.github.io/ai_se_week2_assignment_machine_learning/)**

This project includes a **fully interactive HTML presentation** with speech narration capabilities. The presentation is hosted on GitHub Pages and can be accessed directly through your browser.

### How to Use the Presentation

#### 🔍 **Browser TTS Narration (Free & Instant)**
1. Open the [GitHub Pages link](https://plp-academy.github.io/ai_se_week2_assignment_machine_learning/)
2. Click the **"🎵" voice button** in the top-right corner
3. Select **"🗣️ Browser TTS"** from the voice service options
4. Click the **▶️ Play button** to start narration
5. Adjust **speed and pitch** sliders if desired
6. Use **▶️ Play** and **⏭️ Next** buttons to navigate through slides
7. **Keyboard shortcuts**: Space to play/pause, Arrow keys to navigate

*Works immediately in Chrome, Firefox, Safari, and Edge.*

#### 🔊 **ElevenLabs AI Narration (Premium Natural Voice)**
1. Visit [elevenlabs.io](https://elevenlabs.io) and create a free account (10,000 characters/month)
2. Get your **API key** from ElevenLabs dashboard
3. Open the [presentation](https://plp-academy.github.io/ai_se_week2_assignment_machine_learning/)
4. Click **"🎵" voice button** in the top-right corner
5. Select **"🎯 ElevenLabs AI"** from voice service options
6. **Paste your API key** in the input field
7. Click **▶️ Play button** to hear professional AI narration
8. Use automatic **⏭️ Next** feature to advance slides smoothly

*Premium natural voice with lifelike intonation and expression.*

### 🔧 Local Presentation Setup
To run the presentation locally:
```bash
# Navigate to docs directory
cd docs/

# Open in your default browser
start index.html    # Windows CMD
open index.html     # macOS
xdg-open index.html # Linux
```

### 🎨 Presentation Features
- **10 Interactive Slides** with smooth animations
- **Dual Voice Services** (Browser TTS + ElevenLabs AI)
- **Responsive Design** works on all devices
- **Keyboard Navigation** and touch controls
- **Progress Tracking** with visual progress bar
- **Image Descriptions** for accessible narration
- **Professional Typography** (Google Fonts: Inter & Poppins)

---

## Overview
This project demonstrates how machine learning can advance the UN Sustainable Development Goals, specifically **SDG 11: Sustainable Cities and Communities**. Using K-Means clustering on comprehensive data from all three UN DESA sources (Urban Agglomeration and Capital Cities, Urban Population estimates, and Locations data), it groups cities based on population and sustainability metrics to support informed policy design and urban planning.

## Components
The project is structured into several key components:

- **`data_analysis.ipynb`** → **Comprehensive Jupyter Notebook with AI-Powered Analysis** - Complete ML pipeline, clustering analysis, visualization, AND **automatically generated ethical reflection and summary reports** using AI-driven insights
- **`app.py`** → **Interactive Streamlit Dashboard** - Advanced visualization platform with **AI-generated reports**, real-time clustering adjustments, and comprehensive urban analysis tools
- **`reporting_utils.py`** → **AI Report Generation Module** - Intelligent functions that create dynamic ethical reflections and summary reports based on actual clustering performance and data characteristics
- **`ethical_reflection.md`** → Static ethical considerations document covering bias, fairness, and responsible AI practices
- **`summary_report.md`** → Static project summary with methodology and key findings overview

## How to Run
To set up and run this project:

1.  **Navigate to the project directory:**
    ```bash
    cd AI_SE_week2_assignment
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1 # On Windows PowerShell
    # source .venv/bin/activate # On Linux/macOS
    ```
3.  **Install necessary dependencies:**
    ```bash
    pip install pandas openpyxl scikit-learn matplotlib seaborn streamlit
    ```
    > **Note:** If you are behind a corporate proxy, you may need to configure pip to use proxy settings. For example:
    > ```bash
    > pip install --proxy="http://your-proxy-server:port" pandas openpyxl scikit-learn matplotlib seaborn streamlit
    > ```
    > Replace `"http://your-proxy-server:port"` with your actual proxy configuration.
4.  **Execute the Jupyter Notebook:**
    Open `data_analysis.ipynb` in a Jupyter environment (e.g., VS Code with Python extension, Jupyter Lab, or Jupyter Notebook) and run all cells. This will perform the data analysis, clustering, and generate `clustered_cities.csv` and figures in the `figures/` directory.
5.  **Explore AI-Generated Reports:**
    **In the Notebook**: Run all cells in `data_analysis.ipynb` to see **AI-generated ethical reflection and summary reports** alongside the analysis
    **In the Streamlit App**: Run with automatic report regeneration when clustering parameters change
6.  **Review Documentation:**
    Read the Markdown files (`ethical_reflection.md`, `summary_report.md`) for static documentation. The notebook and app provide **dynamic AI-generated reports**.

## Tools Used
-   **Python**: Programming language
-   **Pandas**: Data manipulation and analysis
-   **Scikit-learn**: Machine learning (K-Means, PCA, StandardScaler)
-   **Matplotlib** & **Seaborn**: Data visualization
-   **Streamlit**: Interactive web application development
-   **Jupyter Notebook**: Interactive development environment

## Core Modules Description
### Data Preprocessing Module
- **Input:** UN DESA Population Division CSV datasets (Urban Population, Locations, Urban Agglomeration)
- **Functions:** Data loading, cleaning, missing value handling, feature selection, and standardization using StandardScaler
- **Output:** Cleaned, scaled feature matrix ready for clustering

### Clustering Module
- **Algorithm:** K-Means clustering (with optional DBSCAN comparison)
- **Process:** Elbow method for optimal k determination, clustering execution, and cluster assignment
- **Evaluation:** Silhouette score, Davies-Bouldin index
- **Feature Engineering:** Population growth rates, urbanization ratios, population scaling metrics

### Visualization Module
- **PCA Visualizations:** 2D/3D cluster scatter plots
- **Interactive Plots:** Plotly-based global scatter plots with hover information
- **Geographic Maps:** Folium-based world maps with cluster markers and color coding
- **Analytics Charts:** Bar/line charts for population trends and feature distributions

### Streamlit App Structure
- **Data Loading:** CSV import with clustering validation
- **User Interface:** Region/country/cluster filters, key metrics display
- **Interactive World Map:** Folium integration with cluster color coding
- **Dashboard:** Key metrics panels, population trend charts, cluster comparisons

## Dependencies and Installation
**Required Libraries:**
- Python 3.8+
- pandas, numpy, openpyxl (data manipulation & Excel reading)
- scikit-learn (clustering, preprocessing, evaluation metrics)
- matplotlib, seaborn (plotting & data visualization)
- plotly (interactive visualizations)
- folium (geographic mapping)
- streamlit (web app framework)
- nbformat (notebook operations)
- ipython (Jupyter environment support)

**Installation:**
```bash
pip install pandas numpy openpyxl scikit-learn matplotlib seaborn plotly folium streamlit nbformat ipython
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Running the System

### Complete Analysis Workflow
1. **Data Processing & ML Analysis**: Execute `data_analysis.ipynb` to run the complete analysis pipeline
2. **AI-Generated Reports**: Notebook automatically creates ethical reflection and summary reports
3. **Interactive Exploration**: Use Streamlit app for advanced visualization and parameter adjustments

### Jupyter Notebook Analysis
```bash
jupyter notebook data_analysis.ipynb
# Features:
# - Complete data preprocessing and clustering
# - ML model evaluation with Silhouette & Davies-Bouldin scores
# - Visualizations (PCA plots, feature analysis)
# - AI-generated ethical reflection and summary reports
# - Generates clustered_cities.csv and figures
```

### Streamlit Application
```bash
streamlit run app.py
# Features:
# - Interactive dashboard with real-time visualizations
# - On-demand K-Means parameter adjustments
# - Geographic clustering analysis with world maps
# - AI-generated reports with automatic regeneration
# - DBSCAN clustering comparison tool
```

### Data Flow Architecture
```
Raw UN DESA Data → Jupyter Analysis → Clustering Results → AI Reports → Streamlit Dashboard
     ↓                    ↓              ↓                   ↓              ↓
Excel Files     Data Processing     `clustered_cities.csv`   Markdown     Interactive
(Data/)           Pipeline               (Data/)           Reports        Exploration
                                                                          (Web App)
```

## Future Improvements
- **Real-time Data Integration:** Connect to live UN data APIs for continuous updates
- **Multi-criteria Sustainability Metrics:** Incorporate environmental indicators (air quality, green spaces), economic factors (GDP per capita), and social metrics (health, education indices)
- **Advanced Clustering Techniques:** DBSCAN for density-based clustering, Hierarchical clustering for dendrogram analysis
- **Geospatial Analysis:** Integrate GIS data for more precise urban boundary definitions
- **Interactive Forecasting:** Time-series modeling for urban growth predictions
- **Cross-cultural Validation:** Community feedback loops for cluster interpretation accuracy
- **Mobile Optimization:** Responsive design for field use by urban planners
- **Multi-language Support:** Localization for global accessibility

## 🤖 AI-Powered Report Generation

### Intelligent Analysis Features
This project features **cutting-edge AI-driven report generation** that automatically creates professional analysis documents based on actual clustering results:

#### Ethical Reflection Reports
- **Adaptive Content**: Reports tailored to your specific clustering performance metrics
- **Real-time Bias Assessment**: Analyzes Silhouette scores and provides contextual recommendations
- **Responsible AI Guidance**: Custom advice based on model quality and data characteristics
- **Data-Driven Insights**: References actual country counts, feature usage, and cluster quality

#### Summary Reports
- **Dynamic Performance Evaluation**: "Excellent", "Good", or "Suboptimal" clustering assessment
- **Intelligent Recommendations**: Context-aware suggestions for improving analysis
- **Live Metrics Integration**: Includes current Silhouette and Davies-Bouldin scores
- **Cluster Distribution Analysis**: Automated breakdown of cluster sizes and percentages

#### Key AI Capabilities
- ✅ **Automatic Report Regeneration** when clustering parameters change
- ✅ **Performance-Based Recommendations** using statistical analysis
- ✅ **Contextual Ethical Assessment** based on model quality metrics
- ✅ **Interactive Exploration** with real-time report updates
- ✅ **Multi-Format Support** (Markdown for notebooks, Streamlit for web interface)

### Usage Examples
```python
# Reports automatically adapt based on your clustering results
if silhouette_score > 0.7:
    # AI generates "Excellent Clustering" assessment with specific recommendations
elif silhouette_score > 0.5:
    # AI generates "Good Clustering" assessment with moderate suggestions
else:
    # AI generates "Suboptimal Clustering" assessment with improvement guidance
```

## SDG 11 Alignment
This project directly supports **Sustainable Development Goal 11** by providing actionable insights for inclusive, safe, resilient, and sustainable cities through data-driven urban planning, enhanced by **AI-powered intelligent analysis and automated report generation**.
