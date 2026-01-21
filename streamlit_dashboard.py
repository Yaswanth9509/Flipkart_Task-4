"""
Maritime Fleet Performance Analytics - Interactive Dashboard
Streamlit-based visualization and analytics dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Maritime Fleet Analytics Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - minimal styling that works in both light and dark mode
st.markdown("""
    <style>
    .stMetric {
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load all available datasets"""
    base_dir = Path(__file__).parent
    data_dir = base_dir / 'data'
    output_dir = base_dir / 'output'
    
    data = {}
    
    # Load integrated data
    if (output_dir / 'integrated_data.csv').exists():
        data['integrated'] = pd.read_csv(output_dir / 'integrated_data.csv')
        if 'Timestamp' in data['integrated'].columns:
            data['integrated']['Timestamp'] = pd.to_datetime(data['integrated']['Timestamp'])
    
    # Load vessel metrics
    if (output_dir / 'vessel_metrics.csv').exists():
        data['metrics'] = pd.read_csv(output_dir / 'vessel_metrics.csv')
    
    # Load summary statistics
    if (output_dir / 'data_summary.csv').exists():
        data['summary'] = pd.read_csv(output_dir / 'data_summary.csv')
    
    return data

# Main dashboard
def main():
    # Header
    st.title("🚢 Maritime Fleet Performance Analytics Dashboard")
    st.markdown("---")
    
    # Load data
    try:
        data = load_data()
        
        if not data:
            st.warning("⚠️ No data available. Please run the analysis first from the main application.")
            st.info("Run `python app.py` and choose option 1 (Quick Analysis) to generate data.")
            return
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Select View",
            ["📊 Overview", "🚢 Fleet Metrics", "📈 Performance Analysis", "⚠️ Risk Assessment", "📋 Data Explorer"]
        )
        
        # Display selected page
        if page == "📊 Overview":
            show_overview(data)
        elif page == "🚢 Fleet Metrics":
            show_fleet_metrics(data)
        elif page == "📈 Performance Analysis":
            show_performance_analysis(data)
        elif page == "⚠️ Risk Assessment":
            show_risk_assessment(data)
        elif page == "📋 Data Explorer":
            show_data_explorer(data)
            
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Please ensure you have run the analysis first using the main application.")

def show_overview(data):
    """Overview page with key metrics"""
    st.header("Fleet Overview")
    
    if 'metrics' in data:
        metrics_df = data['metrics']
        
        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Vessels", len(metrics_df))
        
        with col2:
            avg_efficiency = metrics_df['avg_fuel_efficiency_score'].mean()
            st.metric("Avg Fuel Efficiency", f"{avg_efficiency:.1f}")
        
        with col3:
            total_distance = metrics_df['total_distance'].sum()
            st.metric("Total Distance (nm)", f"{total_distance:,.0f}")
        
        with col4:
            avg_risk = metrics_df['composite_risk_score'].mean()
            st.metric("Average Risk Score", f"{avg_risk:.1f}")
        
        st.markdown("---")
        
        # Charts in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 vessels by fuel efficiency
            st.subheader("Top 10 Vessels by Fuel Efficiency")
            top_vessels = metrics_df.nlargest(10, 'avg_fuel_efficiency_score')[['Vessel_ID', 'avg_fuel_efficiency_score']]
            fig = px.bar(top_vessels, x='Vessel_ID', y='avg_fuel_efficiency_score',
                        color='avg_fuel_efficiency_score',
                        color_continuous_scale='Greens',
                        labels={'avg_fuel_efficiency_score': 'Fuel Efficiency Score'})
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk distribution
            st.subheader("Risk Score Distribution")
            fig = px.histogram(metrics_df, x='composite_risk_score', nbins=20,
                             color_discrete_sequence=['#ef4444'],
                             labels={'composite_risk_score': 'Risk Score', 'count': 'Number of Vessels'})
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

def show_fleet_metrics(data):
    """Fleet metrics detailed view"""
    st.header("Fleet Metrics Analysis")
    
    if 'metrics' not in data:
        st.warning("No metrics data available")
        return
    
    metrics_df = data['metrics']
    
    # Vessel selector
    selected_vessel = st.selectbox("Select Vessel", ['All Vessels'] + list(metrics_df['Vessel_ID'].unique()))
    
    if selected_vessel == 'All Vessels':
        display_df = metrics_df
    else:
        display_df = metrics_df[metrics_df['Vessel_ID'] == selected_vessel]
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Speed (knots)", f"{display_df['avg_speed'].mean():.2f}")
        st.metric("Average Utilization %", f"{display_df['avg_utilization_rate'].mean():.1f}")
    
    with col2:
        st.metric("Engine Health Score", f"{display_df['avg_engine_health'].mean():.1f}")
        st.metric("Average Engine Load %", f"{display_df['avg_engine_load'].mean():.1f}")
    
    with col3:
        st.metric("Total Maintenance Cost", f"${display_df['total_maintenance_cost'].sum():,.0f}")
        st.metric("Total Repair Hours", f"{display_df['total_repair_hours'].sum():,.1f}")
    
    st.markdown("---")
    
    # Scatter plot: Fuel efficiency vs Speed
    st.subheader("Fuel Efficiency vs Average Speed")
    fig = px.scatter(metrics_df, x='avg_speed', y='avg_fuel_efficiency_score',
                    color='composite_risk_score',
                    size='total_distance',
                    hover_data=['Vessel_ID'],
                    color_continuous_scale='RdYlGn_r',
                    labels={'avg_speed': 'Average Speed (knots)',
                           'avg_fuel_efficiency_score': 'Fuel Efficiency Score',
                           'composite_risk_score': 'Risk Score'})
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def show_performance_analysis(data):
    """Performance analysis charts"""
    st.header("Performance Analysis")
    
    if 'metrics' not in data:
        st.warning("No metrics data available")
        return
    
    metrics_df = data['metrics']
    
    # Performance metrics selector
    metric_options = {
        'Fuel Efficiency': 'avg_fuel_efficiency_score',
        'Average Speed': 'avg_speed',
        'Utilization Rate': 'avg_utilization_rate',
        'Engine Health': 'avg_engine_health',
        'Engine Load': 'avg_engine_load'
    }
    
    selected_metric = st.selectbox("Select Performance Metric", list(metric_options.keys()))
    metric_column = metric_options[selected_metric]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot
        st.subheader(f"{selected_metric} Distribution")
        fig = px.box(metrics_df, y=metric_column, 
                    color_discrete_sequence=['#3b82f6'])
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top performers
        st.subheader(f"Top 10 Vessels by {selected_metric}")
        top_performers = metrics_df.nlargest(10, metric_column)[['Vessel_ID', metric_column]]
        fig = px.bar(top_performers, x='Vessel_ID', y=metric_column,
                    color=metric_column,
                    color_continuous_scale='Viridis')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Correlation heatmap
    st.subheader("Performance Metrics Correlation")
    correlation_columns = ['avg_fuel_efficiency_score', 'avg_speed', 'avg_utilization_rate', 
                          'avg_engine_health', 'avg_engine_load', 'composite_risk_score']
    corr_matrix = metrics_df[correlation_columns].corr()
    
    fig = px.imshow(corr_matrix, 
                   text_auto='.2f',
                   color_continuous_scale='RdBu_r',
                   aspect='auto',
                   labels=dict(color="Correlation"))
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def show_risk_assessment(data):
    """Risk assessment dashboard"""
    st.header("Risk Assessment")
    
    if 'metrics' not in data:
        st.warning("No metrics data available")
        return
    
    metrics_df = data['metrics']
    
    # Risk categories
    def categorize_risk(score):
        if score >= 60:
            return 'High Risk'
        elif score >= 40:
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    metrics_df['risk_category'] = metrics_df['composite_risk_score'].apply(categorize_risk)
    
    # Risk distribution
    col1, col2, col3 = st.columns(3)
    
    high_risk = len(metrics_df[metrics_df['risk_category'] == 'High Risk'])
    medium_risk = len(metrics_df[metrics_df['risk_category'] == 'Medium Risk'])
    low_risk = len(metrics_df[metrics_df['risk_category'] == 'Low Risk'])
    
    with col1:
        st.metric("🔴 High Risk Vessels", high_risk)
    with col2:
        st.metric("🟡 Medium Risk Vessels", medium_risk)
    with col3:
        st.metric("🟢 Low Risk Vessels", low_risk)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk category pie chart
        st.subheader("Risk Category Distribution")
        risk_counts = metrics_df['risk_category'].value_counts()
        fig = px.pie(values=risk_counts.values, names=risk_counts.index,
                    color=risk_counts.index,
                    color_discrete_map={'High Risk': '#ef4444', 
                                       'Medium Risk': '#f59e0b',
                                       'Low Risk': '#10b981'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk scores
        st.subheader("Vessel Risk Scores")
        fig = px.scatter(metrics_df, x='Vessel_ID', y='composite_risk_score',
                        color='risk_category',
                        color_discrete_map={'High Risk': '#ef4444', 
                                          'Medium Risk': '#f59e0b',
                                          'Low Risk': '#10b981'},
                        hover_data=['avg_fuel_efficiency_score', 'total_maintenance_cost'])
        fig.update_layout(height=400, xaxis={'tickangle': -45})
        st.plotly_chart(fig, use_container_width=True)
    
    # High risk vessels table
    st.subheader("🔴 High Risk Vessels Details")
    high_risk_vessels = metrics_df[metrics_df['risk_category'] == 'High Risk'].sort_values('composite_risk_score', ascending=False)
    
    if len(high_risk_vessels) > 0:
        st.dataframe(
            high_risk_vessels[['Vessel_ID', 'composite_risk_score', 'avg_fuel_efficiency_score', 
                              'avg_engine_health', 'total_maintenance_cost']].reset_index(drop=True),
            use_container_width=True
        )
    else:
        st.success("No high-risk vessels identified! 🎉")

def show_data_explorer(data):
    """Data explorer with raw data views"""
    st.header("Data Explorer")
    
    # Dataset selector
    available_datasets = list(data.keys())
    selected_dataset = st.selectbox("Select Dataset", available_datasets)
    
    if selected_dataset in data:
        df = data[selected_dataset]
        
        st.subheader(f"Dataset: {selected_dataset}")
        
        # Show basic info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        # Filter options
        st.subheader("Data Filters")
        
        # Column selector for filtering
        if selected_dataset == 'metrics':
            min_risk = st.slider("Minimum Risk Score", 
                               float(df['composite_risk_score'].min()),
                               float(df['composite_risk_score'].max()),
                               float(df['composite_risk_score'].min()))
            filtered_df = df[df['composite_risk_score'] >= min_risk]
        else:
            filtered_df = df
        
        # Display data
        st.subheader("Data Preview")
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"{selected_dataset}_export.csv",
            mime="text/csv"
        )
        
        # Summary statistics
        if st.checkbox("Show Summary Statistics"):
            st.subheader("Summary Statistics")
            st.dataframe(filtered_df.describe(), use_container_width=True)

# Run the app
if __name__ == "__main__":
    main()
