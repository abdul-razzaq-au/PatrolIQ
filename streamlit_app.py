import streamlit as st
import umap
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Crime Analysis Dashboard", layout="wide")
st.title("🚔 Crime Hotspot & Pattern Analysis Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    file_id1 = "12fmWn2T1P9Waa4E5bHd84WKQW0F7tZaz"
    url1 = f"https://drive.google.com/uc?id={file_id1}"
    
    file_id2 = "1eu731YpmZ7UuGOjNANOvPx62en67qbM5"
    url2 = f"https://drive.google.com/uc?id={file_id2}"
    df = pd.read_pickle(url1)      # engineered data
    df_og = pd.read_pickle(url2)     # original data
    return df, df_og

df, df_og = load_data()

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
page = st.sidebar.radio(
    "Select Page",
    [
        "📍 Spatial Analysis",
        "⏱️ Temporal Analysis",
        "📊 Dimensionality Reduction",
        "📈 Model Monitoring"
    ]
)

# =====================================================
# 📍 SPATIAL ANALYSIS
# =====================================================
if page == "📍 Spatial Analysis":

    st.header("📍 Crime Hotspots")

    sample = df_og.sample(5000)

    st.subheader("Cluster Visualization")

    fig = px.scatter_mapbox(
        sample,
        lat="Latitude",
        lon="Longitude",
        color="KMeans_Cluster",
        hover_data=["Primary Type", "Location Description"],
        zoom=10,
        mapbox_style="carto-positron"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔥 Crime Heatmap")

    heatmap = px.density_mapbox(
        sample,
        lat="Latitude",
        lon="Longitude",
        radius=10,
        zoom=10,
        mapbox_style="carto-positron"
    )

    st.plotly_chart(heatmap, use_container_width=True)

    st.subheader("Filter by Cluster")

    cluster = st.selectbox("Select Cluster", sorted(df_og["KMeans_Cluster"].unique()))
    filtered = df_og[df_og["KMeans_Cluster"] == cluster]

    map_df = filtered[["Latitude", "Longitude"]].rename(
        columns={"Latitude": "lat", "Longitude": "lon"}
    )

    st.map(map_df)

    # -------------------------------
    # SPATIAL CLUSTER INTERPRETATION
    # -------------------------------
    st.subheader("🧠 Spatial Cluster Interpretation")

    cluster = st.selectbox(
        "Select Spatial Cluster",
        sorted(df_og["KMeans_Cluster"].unique())
    )

    cluster_df = df_og[df_og["KMeans_Cluster"] == cluster]
    cluster_dfe = df[df["KMeans_Cluster"] == cluster]

    # Top crimes (excluding THEFT)
    filtered = cluster_df[cluster_df["Primary Type"] != "THEFT"]

    top_crimes = (
        filtered["Primary Type"]
        .value_counts()
        .head(3)
        .index.tolist()
    )

    # Dominant features
    top_location = cluster_df["Location Description"].value_counts().idxmax()
    top_crime = cluster_df["Primary Type"].value_counts().idxmax()
    avg_hour = cluster_dfe["Hour"].mean()
    avg_severity = df[df["KMeans_Cluster"] == cluster]["Crime_Severity_Score"].mean()
    location_freq = df[df["KMeans_Cluster"] == cluster]["Location_Desc_freq"].mean()

    # Time pattern
    if avg_hour < 6:
        time_pattern = "🌙 Late-night activity"
    elif avg_hour < 12:
        time_pattern = "🌅 Morning activity"
    elif avg_hour < 18:
        time_pattern = "🌇 Afternoon activity"
    else:
        time_pattern = "🌃 Evening activity"

    st.markdown(f"### Cluster {cluster}")

    st.write("**Dominant Crime:**", top_crime)
    st.write("**Dominant Location:**", top_location)
    st.write("**Time Pattern:**", time_pattern)
    st.write("**Top Crimes (excluding theft):**", ", ".join(top_crimes))
    st.write("**Severity Level:**", round(avg_severity, 2))


    # -------------------------------
    # PATROL STRATEGY
    # -------------------------------
    st.subheader("🚔 Patrol Strategy")

    # Decision logic using multiple features
    if avg_severity > 3:
        st.error("""
        🔴 **High-Risk Crime Zone**
        - Increase police presence
        - Deploy rapid response teams
        - Focus on violent crime prevention
        """)

    elif avg_hour < 6:
        st.warning("""
        🟠 **Late-Night Crime Zone**
        - Increase night patrol
        - Monitor suspicious activity
        - Focus on safety enforcement
        """)

    elif "APARTMENT" in top_location.upper():
        st.error("""
        🔴 **Residential Crime Zone**
        - Community policing
        - Monitor domestic incidents
        - Increase neighborhood patrol
        """)

    elif "STREET" in top_location.upper():
        st.warning("""
        🟡 **Street Crime Zone**
        - Increase mobile patrol units
        - Monitor public areas
        - Prevent theft and robbery
        """)

    elif "STORE" in top_location.upper():
        st.info("""
        🟢 **Retail Theft Zone**
        - CCTV surveillance
        - Coordinate with store security
        - Prevent shoplifting
        """)

    else:
        st.success("""
        🟢 **Moderate Risk Zone**
        - Maintain routine patrol
        - Monitor general activity
        - Prevent opportunistic crimes
        """)

    st.subheader("🔝 Top 10 Crime Types")

    top10 = (
        cluster_df["Primary Type"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(top10)

# =====================================================
# ⏱️ TEMPORAL ANALYSIS
# =====================================================
elif page == "⏱️ Temporal Analysis":

    st.header("⏱️ Temporal Crime Patterns")

    st.subheader("Crimes by Hour")
    st.line_chart(df["Hour"].value_counts().sort_index())

    st.subheader("Crimes by Day of Week")
    st.bar_chart(df["Day_of_Week"].value_counts().sort_index())

    st.subheader("Crimes by Month")
    st.line_chart(df["Month"].value_counts().sort_index())

    st.subheader("Temporal Cluster Distribution")
    st.bar_chart(df["Temporal_Cluster"].value_counts())

    top3 = (
        df_og.groupby("Temporal_Cluster")["Primary Type"]
        .value_counts()
        .groupby(level=0)
        .head(5)
        .rename("Count")
        .reset_index()
    )
    st.subheader("🔍 Top 5 Crime Types per Temporal Cluster")
    st.dataframe(top3, hide_index=True)

    # -------------------------------
    # TEMPORAL CLUSTER INTERPRETATION
    # -------------------------------
    st.subheader("🧠 Temporal Cluster Interpretation")

    t_cluster = st.selectbox(
        "Select Temporal Cluster",
        sorted(df_og["Temporal_Cluster"].unique())
    )

    # Dynamic top crimes (excluding THEFT)
    filtered = df_og[df_og["Primary Type"] != "THEFT"]

    top_crimes = (
        filtered[filtered["Temporal_Cluster"] == t_cluster]["Primary Type"]
        .value_counts()
        .head(3)
        .index.tolist()
    )

    # Base interpretation using your cluster patterns
    temporal_info = {
        0: "🟡 Afternoon mixed crime pattern (weekday activity)",
        1: "❄️ Winter daytime crime pattern (seasonal)",
        2: "🍂 Fall daytime property crime pattern",
        3: "🔴 Late-night high-risk crime pattern",
        4: "🔥 Weekend high-activity crime pattern"
    }

    st.markdown(f"### Cluster {t_cluster}")

    st.write("**Pattern:**", temporal_info.get(t_cluster, "Pattern not defined"))

    st.write("**Top Crimes (excluding theft):**", ", ".join(top_crimes))

    st.subheader("🔝 Top 10 Crime Types")
    
    cluster_df = df_og[df_og["Temporal_Cluster"] == t_cluster]
    top10 = (
        cluster_df["Primary Type"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(top10)

    # -------------------------------
    # PATROL STRATEGY
    # -------------------------------
    st.subheader("🚔 Patrol Strategy")

    if t_cluster == 3:
        st.error("""
        🔴 **High-Risk Zone (Late Night)**
        - Increase night patrol units
        - Deploy rapid response teams
        - Focus on violent crime prevention
        """)

    elif t_cluster == 4:
        st.warning("""
        🔥 **Weekend High Activity Zone**
        - Deploy additional police on weekends
        - Monitor crowded/public areas
        - Prevent robbery and theft incidents
        """)

    elif t_cluster == 1:
        st.info("""
        ❄️ **Winter Crime Pattern**
        - Monitor indoor/commercial areas
        - Focus on fraud and financial crimes
        - Increase daytime surveillance
        """)

    elif t_cluster == 2:
        st.info("""
        🍂 **Property Crime Zone (Fall)**
        - Focus on theft and property damage
        - Increase routine patrols
        - Monitor residential/commercial areas
        """)

    else:
        st.success("""
        🟡 **Moderate Risk Zone**
        - Maintain regular patrol
        - Monitor daytime activity
        - Focus on theft prevention
        """)



# =====================================================
# 📊 DIMENSIONALITY REDUCTION
# =====================================================
elif page == "📊 Dimensionality Reduction":

    st.header("📊 PCA Visualization")

    features = [
        "Latitude_Norm",
        "Longitude_Norm",
        "Hour",
        "Crime_Severity_Score",
        "Location_Desc_freq"
    ]

    X = df[features]

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    df_pca = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
    df_pca["Cluster"] = df["KMeans_Cluster"]

    fig = px.scatter(
        df_pca.sample(5000),
        x="PC1",
        y="PC2",
        color="Cluster",
        title="PCA Projection of Crime Data"
    )

    st.plotly_chart(fig, use_container_width=True)


    st.subheader("🧠 Dimensionality Reduction Insights")

    st.markdown("""
    ### 🔍 PCA (Principal Component Analysis)
    - Captures only **linear relationships**
    - First 2 components explain **~38% variance**
    - Requires **~6 components for 70% variance**
    - ❌ Clusters overlap → not ideal for visualization

    ---

    ### 🔍 t-SNE
    - Captures **non-linear patterns**
    - Shows **distinct local clusters**
    - Good for identifying **hidden structures**
    - ⚠️ Does not preserve global relationships well

    ---

    ### 🔍 UMAP (Best)
    - Preserves **both local & global structure**
    - Produces **clear and compact clusters**
    - Aligns well with **K-Means clustering results**
    - ✅ Best visualization for this dataset

    ---

    ### 🎯 Final Insight
    The dataset contains **complex non-linear patterns**, making PCA insufficient for low-dimensional representation.  
    Non-linear techniques like **t-SNE and UMAP** provide better visualization, with **UMAP giving the most meaningful cluster separation**.
    """)


    st.subheader("🔥 UMAP Visualization (Cluster View)")

    features = [
        "Latitude_Norm",
        "Longitude_Norm",
        "Hour",
        "Crime_Severity_Score",
        "Location_Desc_freq"
    ]
    drop_cols = ['Latitude', 'Longitude', 'Lat_bin', 'Lon_bin', 'Primary Type', 'Date'] 
    
    sample_df = df.sample(50000, random_state=42)
    X = sample_df.drop(columns=drop_cols)
    X = X.select_dtypes(include=['int64', 'float64'])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    @st.cache_data
    def compute_umap(X):
        model = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42)
        return model.fit_transform(X)

    X_umap = compute_umap(X_scaled)

    df_umap = pd.DataFrame(X_umap, columns=["UMAP1", "UMAP2"])
    df_umap["Crime_Type"] = df_og.loc[sample_df.index, "Primary Type"]

    fig = px.scatter(
        df_umap,
        x="UMAP1",
        y="UMAP2",
        color="Crime_Type",
        title="UMAP Projection (Sampled Data)"
    )

    st.plotly_chart(fig, use_container_width=True)    




    # =====================================================
# 📈 MODEL MONITORING
# =====================================================
elif page == "📈 Model Monitoring":

    st.header("📈 Model Performance Dashboard")

    st.subheader("K-Means Model")
    st.metric("Optimal Clusters (K)", 7)

    st.subheader("DBSCAN Model")
    st.metric("Clusters Detected", 7)
    st.metric("Noise Points", 47)

    st.subheader("Hierarchical Clustering")
    st.metric("Best Linkage Method", "Ward")

    st.subheader("MLflow Tracking")

    st.markdown("👉 Open MLflow Dashboard below:")
    st.markdown("[Open MLflow UI](https://dagshub.com/armaaz.au.stats/PatrolIQ.mlflow)")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("Developed for Crime Data Analysis Project 🚔")