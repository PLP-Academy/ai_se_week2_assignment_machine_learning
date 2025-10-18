# Reporting utilities for AI-driven analysis reports
# Used in both Streamlit app and Jupyter notebooks

def generate_ethical_reflection(df, feature_cols, silhouette_score_val, n_clusters):
    """Generate ethical reflection based on current clustering results."""
    n_rows = len(df)
    n_countries = df['Country Code'].unique().shape[0] if 'Country Code' in df.columns else 'N/A'

    # Format silhouette score and quality assessment
    silhouette_formatted = ".3f" if silhouette_score_val else "N/A"
    silhouette_formatted = f"{silhouette_score_val:.3f}" if silhouette_score_val is not None else "N/A"

    quality_assessment = 'Strong cluster separation' if silhouette_score_val and silhouette_score_val > 0.5 else 'Potential cluster overlap concerns'

    # Format counter bias recommendation
    if silhouette_score_val is not None and silhouette_score_val < 0.5:
        counter_bias = f"When Silhouette Score < 0.5 ({silhouette_score_val:.3f}), consider alternative clustering methods"
    elif silhouette_score_val is not None:
        counter_bias = f"Current Silhouette Score ({silhouette_score_val:.3f}) indicates good separation, but continuous monitoring required"
    else:
        counter_bias = "Continuous monitoring required for clustering quality"

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

def generate_summary_report(df, feature_cols, n_clusters, silhouette_score_val, davies_bouldin_val):
    """Generate summary report based on current clustering results."""
    n_rows = len(df)
    cluster_sizes = df['Cluster'].value_counts().sort_index()

    # Format metrics for display
    silhouette_formatted = f"{silhouette_score_val:.3f}" if silhouette_score_val is not None else "N/A"
    davies_formatted = f"{davies_bouldin_val:.3f}" if davies_bouldin_val is not None else "N/A"

    # Format silhouette score interpretation
    silhouette_score_display = f"{silhouette_score_val:.3f}" if silhouette_score_val is not None else "Not computed"
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

    # Format performance interpretations
    if silhouette_score_val is not None:
        silhouette_str = f"{silhouette_score_val:.3f}"
        if silhouette_score_val > 0.7:
            summary += f"- **Excellent Clustering:** Silhouette Score ({silhouette_str}) indicates very strong cluster cohesion and separation\n"
        elif silhouette_score_val > 0.5:
            summary += f"- **Good Clustering:** Silhouette Score ({silhouette_str}) indicates reasonable cluster separation\n"
        else:
            summary += f"- **Suboptimal Clustering:** Silhouette Score ({silhouette_str}) suggests potential overlap - consider adjusting parameters\n"

    if davies_bouldin_val is not None:
        davies_str = f"{davies_bouldin_val:.3f}"
        if davies_bouldin_val < 0.5:
            summary += f"- **Strong Cluster Separation:** Davies-Bouldin Index ({davies_str}) indicates well-separated clusters\n"
        elif davies_bouldin_val < 1.0:
            summary += f"- **Moderate Separation:** Davies-Bouldin Index ({davies_str}) indicates acceptable separation\n"
        else:
            summary += f"- **Weak Separation:** Davies-Bouldin Index ({davies_str}) suggests overlapping clusters\n"

    if silhouette_score_val is None and davies_bouldin_val is None:
        summary += "- **Metrics Not Available:** Silhouette Score and Davies-Bouldin Index could not be computed\n"

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

def display_report_in_notebook(report_content, title="Report"):
    """Display a formatted report in a Jupyter notebook."""
    from IPython.display import display, Markdown, HTML

    print(f"\n{'='*len(title)} {title} {'='*len(title)}")
    display(Markdown(report_content))
    print(f"{'='*(len(title)*2 + 9)}\n")

if __name__ == "__main__":
    # Example usage for testing
    print("Reporting utilities module loaded successfully!")
    print("Use generate_ethical_reflection() and generate_summary_report() functions in your notebooks.")
