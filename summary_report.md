# Clustering Urban Indicators for SDG 11: Sustainable Cities and Communities

## SDG Addressed and Problem Statement
This project addresses **Sustainable Development Goal 11: Sustainable Cities and Communities** by analyzing global population data to identify urbanization patterns. The core problem is the increasing strain on urban infrastructure and resources due to rapid urbanization. By clustering cities based on population and sustainability indicators from UN DESA data, we can provide data-driven insights for effective urban planning and policy development.

## ML Method Used
**K-Means Clustering** (unsupervised machine learning) was applied to segment global urban areas into distinct groups based on demographic and urbanization indicators. The analysis included:
- Feature engineering (population growth rates, urbanization ratios, population scaling)
- Data preprocessing (standardization, missing value handling)
- Optimal cluster determination using the Elbow Method
- Model evaluation using Silhouette Score and Davies-Bouldin Index
- Visualization via PCA scatter plots with Plotly for global scatter plots and Folium for interactive world maps
- **Optional DBSCAN clustering** was also implemented for comparison, offering a density-based approach to identify clusters without pre-defining their number, and detecting noise.

## Main Findings and Visual Insights
### Clustering Results:
- **Number of Clusters Identified (K-Means):** 3 optimal clusters (determined by Elbow Method)
- **Silhouette Score (K-Means):** 0.77 (indicating good cluster separation)
- **Key Insights:**
  - **Cluster 0 (High Growth Cities):** Characterized by rapid population increases (high growth rates), medium urbanization ratios, and larger population scales. These cities show aggressive urbanization requiring immediate infrastructure investment and sustainable resource management.
  - **Cluster 1 (Stable/Capital Cities):** Features moderate growth with higher urbanization ratios and variable population scales. These represent established urban centers needing quality-of-life maintenance and green initiatives.
  - **Cluster 2 (Emerging/Smaller Cities):** Exhibits slower growth rates, lower urbanization but potential for scaled development and new infrastructure planning.

### Visualizations Provided:
- **Histograms:** Show distributions of scaled features.
- **Correlation Heatmap:** Identifies relationships between sustainability indicators.
- **Scatter Matrix:** Visualizes relationships between a subset of scaled features.
- **PCA Visualization:** 2D representation of K-Means cluster separation in principal component space.
- **Feature Means Comparison:** Bar charts contrasting average values across K-Means clusters.
- **Interactive PCA Clusters (Plotly):** Allows interactive exploration of K-Means clusters with hover details for urban agglomerations and countries.
- **Folium World Map with Cluster Markers:** Geographic distribution of K-Means clusters, color-coded on an interactive world map.
- **DBSCAN PCA Visualization:** 2D representation of DBSCAN clusters (noise excluded) for comparison.

## Model Evaluation Results
- **K-Means Silhouette Score:** 0.77 (well above the 0.5 threshold, indicating strong cluster cohesion)
- **K-Means Davies-Bouldin Index:** 0.27 (lower values indicate better separation between clusters)
- **DBSCAN Silhouette Score:** (If computed, will be displayed in the notebook/app for comparison)

These metrics confirm the clustering model effectively distinguishes urban development archetypes globally.

## Contribution to Sustainable Urban Planning
This analysis enables:
1. **Targeted Policy Development:** Countries can prioritize investment in high-growth cities while sustaining established urban centers.
2. **Regional Comparisons:** Identify which regions (e.g., Africa vs. Asia vs. Americas) exhibit similar urbanization challenges.
3. **Resource Allocation:** Efficiently distribute funding based on development cluster characteristics.
4. **Monitoring Framework:** Track how cities transition between clusters over time with updated data.
5. **SDG 11 Alignment:** Directly supports making cities more inclusive, safe, resilient, and sustainable through data-driven planning.

The approach demonstrates how artificial intelligence can transform complex population datasets into actionable insights for achieving sustainable development goals globally.
