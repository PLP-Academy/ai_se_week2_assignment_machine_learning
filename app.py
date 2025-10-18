import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, davies_bouldin_score
import plotly.express as px
import folium
from folium.plugins import MarkerCluster

# -------------------------------------------------------------
# Streamlit Page Configuration
# -------------------------------------------------------------
st.set_page_config(layout="wide", page_title="AI for Sustainable Cities (SDG 11)")

# -------------------------------------------------------------
# Title and Context
# -------------------------------------------------------------
st.title("AI for Sustainable Cities (SDG 11)")
st.markdown(
    """
This interactive dashboard supports Sustainable Development Goal 11:
Sustainable Cities and Communities. It visualizes clustering results for cities/countries
based on population and sustainability indicators.

To use this app:
1. Execute the Jupyter notebook (data_analysis.ipynb) to generate `clustered_cities.csv`, or
2. Upload a prepared `clustered_cities.csv` below, or
3. Provide a path to your CSV on disk.
"""
)

# -------------------------------------------------------------
# Data Loading Utilities
# -------------------------------------------------------------
DEFAULT_CSV_PATH = "data/clustered_cities.csv"

@st.cache_data(show_spinner=False)
def load_csv_from_bytes(file_bytes: bytes) -> pd.DataFrame:
    from io import BytesIO
    return pd.read_csv(BytesIO(file_bytes))

@st.cache_data(show_spinner=False)
def load_csv_from_path(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

# Sidebar: Data source controls
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload clustered_cities.csv", type=["csv"]) 
path_input = st.sidebar.text_input("Or provide a path to clustered_cities.csv", value=DEFAULT_CSV_PATH)

# Attempt to load data with priority: uploaded -> path -> default
df: Optional[pd.DataFrame] = None
load_error: Optional[str] = None

# Data Loading (assuming files are in 'data/' directory)
file_path_urban_agglomeration = 'data/WUP2018-DataSource-UrbanAgglomeration-and-CapitalCities.xls'
file_path_urban_population = 'data/WUP2018-DataSource-UrbanPopulation.xls'
file_path_locations = 'data/WUP2018-F00-LOCATIONS.xlsx'

# Initialize dataframes
df_urban_agglomeration = pd.DataFrame()
df_urban_population = pd.DataFrame()
df_locations = pd.DataFrame()

try:
    df_urban_agglomeration = pd.read_excel(file_path_urban_agglomeration, sheet_name='Data', skiprows=16, header=0)
    df_urban_agglomeration.rename(columns={'Location name': 'Urban Agglomeration'}, inplace=True)
    df_urban_agglomeration.dropna(subset=['Urban Agglomeration'], inplace=True)
    df_urban_agglomeration['Country Code'] = df_urban_agglomeration['Country Code'].astype(str)
except Exception as e:
    st.error(f"Error reading {file_path_urban_agglomeration}: {e}")
    df_urban_agglomeration = pd.DataFrame() # Ensure df is a DataFrame even on error

try:
    df_urban_population = pd.read_excel(file_path_urban_population, sheet_name='Data', skiprows=16, header=0)
    df_urban_population.rename(columns={'Data': 'Urban Population'}, inplace=True) # Assuming 'Data' is the urban population value
    # No 'Urban Agglomeration' in this file, so no dropna on it
    df_urban_population['Country Code'] = df_urban_population['Country Code'].astype(str)
except Exception as e:
    st.error(f"Error reading {file_path_urban_population}: {e}")
    df_urban_population = pd.DataFrame() # Ensure df is a DataFrame even on error

try:
    df_locations = pd.read_excel(file_path_locations, sheet_name='Location', skiprows=16, header=0)
    df_locations.rename(columns={'Region, subregion, country or area': 'Country Code', 'Name': 'City'}, inplace=True)
    df_locations.dropna(subset=['City'], inplace=True)
    df_locations['Country Code'] = df_locations['Country Code'].astype(str)
except Exception as e:
    st.error(f"Error reading {file_path_locations}: {e}")
    df_locations = pd.DataFrame() # Ensure df is a DataFrame even on error

# Revised Merge logic
df_combined = pd.DataFrame()
if not df_urban_agglomeration.empty and not df_locations.empty:
    # Merge urban agglomeration data with location data
    df_combined = pd.merge(df_urban_agglomeration, df_locations, 
                           left_on=['Country Code', 'Urban Agglomeration'], 
                           right_on=['Country Code', 'City'], 
                           how='left', suffixes=('_agg', '_loc'))
    if 'City' in df_combined.columns:
        df_combined.drop(columns=['City'], inplace=True)
else:
    st.warning("Could not merge urban agglomeration and location data. Check source files.")

if not df_combined.empty and not df_urban_population.empty:
    # Merge with urban population data at country level
    df = pd.merge(df_combined, df_urban_population[['Country Code', 'Urban Population']], 
                  on='Country Code', how='left')
else:
    df = df_combined.copy() # If urban population data is missing, proceed with what's available

# Handle missing values (example: drop rows with too many NaNs or fill with mean/median)
if not df.empty:
    df.dropna(axis=1, how='all', inplace=True) # Drop columns that are entirely NaN
    df.dropna(axis=0, how='any', subset=[col for col in df.columns if col not in ['Country Code', 'Urban Agglomeration']], inplace=True) # Drop rows with NaN in features used for clustering

if df.empty:
    if load_error:
        st.error(load_error)
    st.info(
        """
No data loaded yet.
- Run data_analysis.ipynb to create clustered_cities.csv in this folder, then refresh, or
- Use the sidebar to upload the CSV or provide a valid file path.
        """
    )
    st.stop()

assert df is not None

# -------------------------------------------------------------
# Basic Validation and Feature Selection
# -------------------------------------------------------------
# Identify numeric feature columns, excluding non-feature helpers
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
excluded_cols = {"cluster", "pca1", "pca2", "latitude", "longitude", "lat", "lon", "long"}
feature_cols = [c for c in numeric_cols if c.lower() not in excluded_cols]

if not feature_cols:
    st.error("No numeric feature columns found for analysis. Ensure your CSV includes numeric indicators.")
    st.stop()

# If clusters are not present, allow on-the-fly clustering
if "Cluster" not in df.columns:
    st.warning("'Cluster' column not found. The app will perform K-Means clustering on the fly.")
    n_clusters = st.sidebar.slider("Number of clusters (KMeans)", min_value=2, max_value=10, value=3, step=1)

    # Track parameter changes for auto-regeneration
    current_params = {"n_clusters": n_clusters, "data_shape": df.shape, "feature_count": len(feature_cols)}

    # Check if parameters changed from previous run
    if 'last_params' not in st.session_state or st.session_state.last_params != current_params:
        # Clear cached reports when parameters change
        if 'ethical_report' in st.session_state:
            del st.session_state.ethical_report
        if 'summary_report' in st.session_state:
            del st.session_state.summary_report
        st.session_state.last_params = current_params

    # Scale and cluster
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["Cluster"] = km.fit_predict(X_scaled)
else:
    # Track data changes for existing clustered data
    current_params = {"data_shape": df.shape, "feature_count": len(feature_cols), "cluster_count": df['Cluster'].nunique()}

    if 'last_params' not in st.session_state or st.session_state.last_params != current_params:
        if 'ethical_report' in st.session_state:
            del st.session_state.ethical_report
        if 'summary_report' in st.session_state:
            del st.session_state.summary_report
        st.session_state.last_params = current_params

    # Still scale data for metrics and PCA
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])

# -------------------------------------------------------------
# Metrics (Silhouette, Davies-Bouldin)
# -------------------------------------------------------------
silhouette_score_val = None
davies_bouldin_val = None
try:
    labels = df["Cluster"].to_numpy().astype(int, copy=False)
except Exception:
    labels, _ = pd.factorize(df["Cluster"])

try:
    if len(np.unique(labels)) > 1 and X_scaled.shape[0] > X_scaled.shape[1]:
        silhouette_score_val = silhouette_score(X_scaled, labels)
        davies_bouldin_val = davies_bouldin_score(X_scaled, labels)
except Exception:
    # Keep as None if computation fails due to edge cases
    pass

# -------------------------------------------------------------
# PCA projection (use provided columns if any, otherwise compute)
# -------------------------------------------------------------
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

if {"PCA1", "PCA2"}.issubset(df.columns):
    pca_df = df[["PCA1", "PCA2", "Cluster"]].copy()
    # Ensure PCA1/PCA2 from file are aligned with X_pca if needed, or just use X_pca
    # For simplicity, we'll prioritize the computed X_pca for consistency in visualizations
    pca_df['PCA1'] = X_pca[:, 0]
    pca_df['PCA2'] = X_pca[:, 1]
else:
    pca_df = pd.DataFrame(X_pca, columns=["PCA1", "PCA2"]) 
    pca_df["Cluster"] = labels

# -------------------------------------------------------------
# Sidebar: Overview & Filtering
# -------------------------------------------------------------
st.sidebar.header("Data Overview")
st.sidebar.write(f"Rows: {len(df):,}")
st.sidebar.write(f"Numeric features: {len(feature_cols)}")
st.sidebar.write(f"Clusters: {df['Cluster'].nunique()}")

selected_clusters = st.sidebar.multiselect(
    "Select clusters to display",
    options=sorted(df["Cluster"].unique().tolist()),
    default=sorted(df["Cluster"].unique().tolist())
)

# Filter data based on selected clusters
mask = df["Cluster"].isin(selected_clusters)
filtered_df = df.loc[mask].copy()

# Recompute PCA on filtered data to ensure index alignment
if not filtered_df.empty:
    filtered_scaler = StandardScaler()
    filtered_X_scaled = filtered_scaler.fit_transform(filtered_df[feature_cols])
    filtered_pca = PCA(n_components=2, random_state=42)
    filtered_X_pca = filtered_pca.fit_transform(filtered_X_scaled)
    filtered_pca_df = pd.DataFrame(filtered_X_pca, columns=["PCA1", "PCA2"], index=filtered_df.index)
    filtered_pca_df["Cluster"] = filtered_df["Cluster"].values

    # Add PCA columns to filtered_df for Plotly visualization
    filtered_df["PCA1"] = filtered_pca_df["PCA1"]
    filtered_df["PCA2"] = filtered_pca_df["PCA2"]
else:
    filtered_pca_df = pd.DataFrame()

# -------------------------------------------------------------
# Summary Section
# -------------------------------------------------------------
st.header("Clustering Summary")
metrics_md = [
    f"- Number of Clusters Identified: {df['Cluster'].nunique()}",
]
if silhouette_score_val is not None:
    metrics_md.append(f"- Silhouette Score: {silhouette_score_val:.3f}")
else:
    metrics_md.append("- Silhouette Score: N/A")
if davies_bouldin_val is not None:
    metrics_md.append(f"- Davies-Bouldin Index: {davies_bouldin_val:.3f}")
else:
    metrics_md.append("- Davies-Bouldin Index: N/A")

st.markdown("\n".join(metrics_md))

# -------------------------------------------------------------
# Visualizations
# -------------------------------------------------------------
st.header("Visualizations")

# PCA Scatterplot
st.subheader("2D PCA Visualization of K-Means Clusters")
fig_pca, ax_pca = plt.subplots(figsize=(10, 7))
sns.scatterplot(
    x="PCA1", y="PCA2", hue="Cluster", data=filtered_pca_df,
    palette="viridis", s=90, alpha=0.8, ax=ax_pca
)
ax_pca.set_title("K-Means Clusters Visualized with PCA")
ax_pca.set_xlabel("Principal Component 1")
ax_pca.set_ylabel("Principal Component 2")
ax_pca.legend(title="Cluster", loc="best")
st.pyplot(fig_pca, clear_figure=True)

# Plotly Interactive PCA Scatter Plot
st.subheader("Interactive PCA Clusters (Plotly)")
if not filtered_df.empty and "Urban Agglomeration" in filtered_df.columns and "Country or area" in filtered_df.columns:
    fig_plotly = px.scatter(filtered_df, x='PCA1', y='PCA2', color='Cluster',
                            hover_name='Urban Agglomeration', hover_data=['Country or area', 'Urban Population'],
                            title='Interactive PCA Clusters (Plotly)',
                            color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig_plotly, use_container_width=True)
else:
    st.info("Required columns for Plotly interactive scatter plot not found or data is empty.")

# Feature Means by Cluster
st.subheader("Feature Means by Cluster")
if feature_cols:
    # Limit to top-N features by variance for readability
    variances = pd.Series(np.var(X_scaled, axis=0), index=feature_cols)
    top_features = variances.sort_values(ascending=False).head(10).index.tolist()
    cluster_means = filtered_df.groupby("Cluster")[top_features].mean().T
    fig_bar, ax_bar = plt.subplots(figsize=(14, 7))
    cluster_means.plot(kind="bar", ax=ax_bar, colormap="viridis")
    ax_bar.set_title("Feature Means by Cluster (Top 10 Var Features)")
    ax_bar.set_xlabel("Features")
    ax_bar.set_ylabel("Mean Value")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig_bar, clear_figure=True)
else:
    st.info("No suitable numeric features found for mean plot.")

# Folium World Map with Cluster Markers
st.subheader("Geographic Distribution of Clusters (Folium Map)")
lat_candidates = ["Latitude", "Lat", "latitude", "lat"]
lon_candidates = ["Longitude", "Lon", "Long", "longitude", "lon", "long"]
lat_col = next((c for c in lat_candidates if c in df.columns), None)
lon_col = next((c for c in lon_candidates if c in df.columns), None)

if bool(lat_col) and bool(lon_col) and not filtered_df.empty:
    # Create a base map
    world_map = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
    marker_cluster = MarkerCluster().add_to(world_map)

    # Add markers for each city
    for idx, row in filtered_df.iterrows():
        if pd.notna(row[lat_col]) and pd.notna(row[lon_col]):
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=f"<b>City:</b> {row['Urban Agglomeration']}<br><b>Country:</b> {row['Country or area']}<br><b>Cluster:</b> {row['Cluster']}",
                icon=folium.Icon(color=px.colors.sequential.Viridis[row['Cluster'] % len(px.colors.sequential.Viridis)], icon='info-sign')
            ).add_to(marker_cluster)
    
    st.folium_static(world_map)
else:
    st.info("Latitude/Longitude columns not found or data is empty. Add lat/lon columns to enable the map.")

# DBSCAN Clustering Section
st.header("DBSCAN Clustering (Optional Comparison)")
st.markdown("DBSCAN is a density-based clustering algorithm. Unlike K-Means, it does not require specifying the number of clusters beforehand and can identify noise points.")

# Sidebar controls for DBSCAN
st.sidebar.subheader("DBSCAN Parameters")
eps = st.sidebar.slider("Epsilon (eps)", min_value=0.1, max_value=5.0, value=0.5, step=0.1)
min_samples = st.sidebar.slider("Min Samples", min_value=2, max_value=20, value=5, step=1)

if st.sidebar.button("Run DBSCAN"):
    with st.spinner("Running DBSCAN..."):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        dbscan_clusters = dbscan.fit_predict(X_scaled)
        
        df["DBSCAN_Cluster"] = dbscan_clusters
        
        n_clusters_dbscan = len(set(dbscan_clusters)) - (1 if -1 in dbscan_clusters else 0)
        n_noise = list(dbscan_clusters).count(-1)
        
        st.write(f"DBSCAN Estimated number of clusters: {n_clusters_dbscan}")
        st.write(f"DBSCAN Estimated number of noise points: {n_noise}")
        
        if n_clusters_dbscan > 1:
            dbscan_silhouette_avg = silhouette_score(X_scaled, dbscan_clusters)
            st.write(f"DBSCAN Silhouette Score: {dbscan_silhouette_avg:.3f}")
            
            # Visualize DBSCAN results with PCA
            dbscan_pca_df = pd.DataFrame(data=X_pca, columns=["PCA1", "PCA2"])
            dbscan_pca_df["Cluster"] = dbscan_clusters
            
            fig_dbscan_pca, ax_dbscan_pca = plt.subplots(figsize=(10, 7))
            mask_dbscan = dbscan_clusters != -1
            sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', data=dbscan_pca_df[mask_dbscan], 
                            palette='viridis', s=90, alpha=0.8, ax=ax_dbscan_pca)
            ax_dbscan_pca.set_title('DBSCAN Clusters Visualized with PCA (Noise Excluded)')
            ax_dbscan_pca.set_xlabel('Principal Component 1')
            ax_dbscan_pca.set_ylabel('Principal Component 2')
            ax_dbscan_pca.legend(title='DBSCAN Cluster', loc='best')
            st.pyplot(fig_dbscan_pca, clear_figure=True)
        else:
            st.info("DBSCAN did not form more than one cluster or only found noise points with current parameters.")

# -------------------------------------------------------------
# Generate Ethical Reflection Report
# -------------------------------------------------------------
def generate_ethical_reflection(df, feature_cols, silhouette_score_val, n_clusters):
    """Generate ethical reflection based on current clustering results."""
    n_rows = len(df)
    n_countries = df['Country Code'].unique().shape[0] if 'Country Code' in df.columns else 'N/A'

    # Format silhouette score and quality assessment
    silhouette_formatted = f"{silhouette_score_val:.3f}" if silhouette_score_val else "N/A"
    quality_assessment = 'Strong cluster separation' if silhouette_score_val and silhouette_score_val > 0.5 else 'Potential cluster overlap concerns'

    # Format counter bias recommendation
    if silhouette_score_val and silhouette_score_val < 0.5:
        counter_bias = f"When Silhouette Score < 0.5 ({silhouette_score_val:.3f}), consider alternative clustering methods"
    else:
        counter_bias = f"Current Silhouette Score ({silhouette_score_val:.3f}) indicates good separation, but continuous monitoring required" if silhouette_score_val else "Continuous monitoring required for clustering quality"

    reflection = f"""# Ethical Reflection: AI for Sustainable Cities (SDG 11)

## Data Bias
The UN DESA Population Division data contains **{n_rows} urban agglomerations** from approximately **{n_countries} countries**. Potential biases include:

### Current Analysis Concerns:
- **Data Completeness:** {len(feature_cols)} numeric features used for clustering
- **Geographic Coverage:** Cities vary significantly in reporting quality and completeness
- **Temporal Challenges:** Analysis based on historical data may not capture recent trends
- **Over-simplification Risk:** K-Means clustering reduces complex urban systems into **{n_clusters} discrete groups**

### Algorithmic Risks with Current Model:
- **Silhouette Score: {silhouette_formatted}** - {quality_assessment}
- **Misclassification Risk:** Cities near cluster boundaries may receive suboptimal interventions
- **Bias Propagation:** Statistical methods may amplify existing data collection disparities

## Fairness: Ensuring Developing Regions Are Not Misrepresented

### Current Clustering Challenges:
- **Representation Disparity:** Only {n_countries} countries represented, may under-sample developing regions
- **False Precision:** Statistical scores don't account for local context and unique challenges
- **Equity Impact:** Clustering could lead to under-resourcing of underrepresented urban areas

## Sustainability Impact and Responsible AI Practices

### Recommendations for Current Implementation:
1. **Counter Bias:** {counter_bias}
2. **Transparent Methodology:** Document all preprocessing and parameter choices
3. **Stakeholder Collaboration:** Involve local urban experts for cluster interpretation
4. **Continuous Updating:** Reassess clusters with new data to capture evolving trends
5. **Holistic Planning:** Use clustering as one of multiple tools for urban planning decisions

## Mitigation Strategies
- **Data Enrichment:** Supplement official statistics with alternative community-led sources
- **Algorithm Transparency:** Clear documentation of clustering methodology and limitations
- **Human Oversight:** Expert review of cluster interpretations before policy implementation
- **Global Capacity Building:** Support improved data collection in underrepresented regions"""
    return reflection

# -------------------------------------------------------------
# Generate Summary Report
# -------------------------------------------------------------
def generate_summary_report(df, feature_cols, n_clusters, silhouette_score_val, davies_bouldin_val):
    """Generate summary report based on current clustering results."""
    n_rows = len(df)
    cluster_sizes = df['Cluster'].value_counts().sort_index()

    # Format metrics for f-string
    silhouette_formatted = f"{silhouette_score_val:.3f}" if silhouette_score_val else "N/A"
    davies_formatted = f"{davies_bouldin_val:.3f}" if davies_bouldin_val else "N/A"

    # Format silhouette score interpretation
    silhouette_score_display = f"{silhouette_score_val:.3f}" if silhouette_score_val else "Not computed"
    separation_quality = "Strong separation" if silhouette_score_val and silhouette_score_val > 0.5 else "May need adjustment"

    summary = f"""# Clustering Urban Indicators for SDG 11: Sustainable Cities and Communities

## SDG Addressed and Problem Statement
This project addresses **Sustainable Development Goal 11: Sustainable Cities and Communities** by analyzing global population data to identify urbanization patterns. The current analysis processed **{n_rows} urban agglomerations** using **{len(feature_cols)} features** and identified **{n_clusters} distinct clusters**.

## ML Method Used
**K-Means Clustering** was applied with the following configuration:
- **Clusters Identified:** {n_clusters}
- **Features Analyzed:** {', '.join(feature_cols[:5])}{'...' if len(feature_cols) > 5 else ''}
- **Data Preprocessing:** Standardization and missing value removal
- **Evaluation Metrics:**
  - Silhouette Score: {silhouette_formatted}
  - Davies-Bouldin Index: {davies_formatted}

## Main Findings and Visual Insights

### Clustering Results:
- **Number of Clusters:** {n_clusters}
- **Silhouette Score:** {silhouette_score_display} ({separation_quality})
- **Cluster Distribution:**
"""

    for i, size in cluster_sizes.items():
        summary += f"  - Cluster {i}: {size} cities ({size/n_rows*100:.1f}%)\n"

    summary += """

### Current Model Performance:
"""

    # Format performance interpretations outside f-strings
    if silhouette_score_val:
        silhouette_str = f"{silhouette_score_val:.3f}"
        if silhouette_score_val > 0.7:
            summary += f"- **Excellent Clustering:** Silhouette Score ({silhouette_str}) indicates very strong cluster cohesion and separation\n"
        elif silhouette_score_val > 0.5:
            summary += f"- **Good Clustering:** Silhouette Score ({silhouette_str}) indicates reasonable cluster separation\n"
        else:
            summary += f"- **Suboptimal Clustering:** Silhouette Score ({silhouette_str}) suggests potential overlap - consider adjusting parameters\n"

    if davies_bouldin_val:
        davies_str = f"{davies_bouldin_val:.3f}"
        if davies_bouldin_val < 0.5:
            summary += f"- **Strong Cluster Separation:** Davies-Bouldin Index ({davies_str}) indicates well-separated clusters\n"
        elif davies_bouldin_val < 1.0:
            summary += f"- **Moderate Separation:** Davies-Bouldin Index ({davies_str}) indicates acceptable separation\n"
        else:
            summary += f"- **Weak Separation:** Davies-Bouldin Index ({davies_str}) suggests overlapping clusters\n"

    summary += f"""

## Contribution to Sustainable Urban Planning

### Actionable Insights from Current Clustering:
1. **{n_clusters} Urban Development Archetypes:** Cities grouped by similar sustainability challenges
2. **Targeted Interventions:** Resource allocation based on cluster characteristics
3. **Global Comparative Analysis:** Benchmarking across similar urban development stages
4. **SDG 11 Progress Tracking:** Evidence-based monitoring of sustainable urbanization goals

### Recommended Next Steps:
- Validate cluster interpretations with urban development experts
- Consider adjusting clustering parameters for improved separation
- Integrate with additional data sources for more comprehensive analysis
- Monitor cluster transitions over time with updated data"""

    return summary

# -------------------------------------------------------------
# Auto-Generated Reports Section
# -------------------------------------------------------------
st.header("AI-Generated Reports")

# Generate Ethical Reflection
st.subheader("Ethical Reflection Report")
if st.button("Regenerate Ethical Reflection", key="ethical"):
    with st.spinner("Generating ethical reflection..."):
        ethical_report = generate_ethical_reflection(df, feature_cols, silhouette_score_val, df['Cluster'].nunique())
        st.markdown(ethical_report)

# Store ethical report in session state for persistence
if 'ethical_report' not in st.session_state:
    st.session_state.ethical_report = generate_ethical_reflection(df, feature_cols, silhouette_score_val, df['Cluster'].nunique())

st.markdown(st.session_state.ethical_report)

# Generate Summary Report
st.subheader("Summary Report")
if st.button("Regenerate Summary Report", key="summary"):
    with st.spinner("Generating summary report..."):
        summary_report = generate_summary_report(df, feature_cols, df['Cluster'].nunique(), silhouette_score_val, davies_bouldin_val)
        st.session_state.summary_report = summary_report

# Store summary report in session state
if 'summary_report' not in st.session_state:
    st.session_state.summary_report = generate_summary_report(df, feature_cols, df['Cluster'].nunique(), silhouette_score_val, davies_bouldin_val)

st.markdown(st.session_state.summary_report)

# Information about auto-regeneration
st.info("💡 Reports auto-regenerate when clustering parameters or data changes. Use buttons above to manual refresh.")

# -------------------------------------------------------------
# Narrative Sections
# -------------------------------------------------------------
st.markdown("---")
st.header("About this project")
st.markdown(
    """
This project leverages unsupervised machine learning (K-Means clustering) to analyze
urban population and sustainability indicators. The workflow:
- Clean, standardize, and analyze indicators in the notebook
- Generate `clustered_cities.csv` with cluster labels (and optionally PCA1/PCA2)
- Explore results interactively in this dashboard
    """
)

st.header("How clustering helps sustainable development")
st.markdown(
    """
- Tailor interventions across similar cities
- Allocate resources efficiently
- Benchmark progress across peer groups
- Provide data-driven insights aligned with SDG 11 targets
    """
)

st.header("Ethical considerations")
st.markdown(
    """
See the accompanying `ethical_reflection.md` for discussion of data bias, fairness,
transparency, and sustainability impacts.
    """
)

st.markdown("---")
st.markdown("Developed for AI for Sustainable Cities (SDG 11) Project")
