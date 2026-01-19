"""
Analytics Engine
Combined metrics calculation, risk assessment, and exploratory analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


class AnalyticsEngine:
    """Unified metrics, risk assessment, and analysis"""
    
    def __init__(self, df, output_dir):
        self.df = df
        self.output_dir = output_dir
        self.metrics = {}
        sns.set_style("whitegrid")
        sns.set_palette("husl")
    
    def calculate_all_metrics(self):
        """Calculate all performance and risk metrics"""
        print("\n" + "="*70)
        print("CALCULATING METRICS & ANALYTICS")
        print("="*70)
        
        self._calculate_fuel_metrics()
        self._calculate_operational_metrics()
        self._calculate_engine_metrics()
        self._calculate_environmental_metrics()
        self._calculate_maintenance_metrics()
        self._calculate_risk_metrics()
        
        return pd.DataFrame(self.metrics)
    
    def _calculate_fuel_metrics(self):
        """Fuel efficiency metrics"""
        self.metrics['fuel_nm_per_liter'] = self.df.groupby('Vessel_ID').apply(
            lambda x: (x['Distance_covered_nm'].sum() / x['Fuel_Used_per_NM_liters'].sum()) 
            if x['Fuel_Used_per_NM_liters'].sum() > 0 else 0
        )
        self.metrics['avg_fuel_efficiency_score'] = self.df.groupby('Vessel_ID')['Fuel_Efficiency_Score'].mean()
    
    def _calculate_operational_metrics(self):
        """Operational performance"""
        self.metrics['avg_speed'] = self.df.groupby('Vessel_ID')['Speed_knots'].mean()
        self.metrics['avg_utilization_rate'] = self.df.groupby('Vessel_ID')['Vessel_Utilization_Rate'].mean()
        self.metrics['total_distance'] = self.df.groupby('Vessel_ID')['Distance_covered_nm'].sum()
    
    def _calculate_engine_metrics(self):
        """Engine health"""
        self.metrics['avg_engine_health'] = self.df.groupby('Vessel_ID')['Engine_Health_Score'].mean()
        self.metrics['avg_engine_load'] = self.df.groupby('Vessel_ID')['Engine_Load_percent'].mean()
    
    def _calculate_environmental_metrics(self):
        """Environmental impact"""
        self.metrics['avg_wave_height'] = self.df.groupby('Vessel_ID')['Wave_Height_meters'].mean()
        self.metrics['avg_navigation_difficulty'] = self.df.groupby('Vessel_ID')['Navigation_Difficulty'].mean()
    
    def _calculate_maintenance_metrics(self):
        """Maintenance costs"""
        self.metrics['total_maintenance_cost'] = self.df.groupby('Vessel_ID')['Maintenance_Cost_USD'].sum()
        self.metrics['total_repair_hours'] = self.df.groupby('Vessel_ID')['Repair_Time_hours'].sum()
    
    def _calculate_risk_metrics(self):
        """Risk assessment"""
        metrics_df = pd.DataFrame(self.metrics)
        
        engine_risk = 100 - metrics_df['avg_engine_health'].fillna(75)
        maintenance_risk = (metrics_df['total_maintenance_cost'].fillna(0) / 10000).clip(0, 100)
        storm_risk = self.df.groupby('Vessel_ID')['Storm_Risk_Index'].mean()
        
        self.metrics['composite_risk_score'] = (
            engine_risk * 0.35 + maintenance_risk * 0.25 + storm_risk * 0.25 +
            metrics_df['avg_engine_load'].fillna(50) / 100 * 100 * 0.15
        ).clip(0, 100)
    
    def generate_visualizations(self, num_charts=5):
        """Generate key visualizations"""
        print("\nGenerating visualizations...")
        
        if num_charts >= 1:
            self._plot_speed_distribution()
        if num_charts >= 2:
            self._plot_fuel_efficiency()
        if num_charts >= 3:
            self._plot_risk_distribution()
        if num_charts >= 4:
            self._plot_engine_health()
        if num_charts >= 5:
            self._plot_correlation()
        
        print(f"Generated {num_charts} visualizations")
    
    def _plot_speed_distribution(self):
        """Speed by vessel type"""
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=self.df, x='Type', y='Speed_knots', ax=ax)
        ax.set_title("Speed Distribution by Vessel Type")
        self._save_plot(fig, "01_speed_distribution")
    
    def _plot_fuel_efficiency(self):
        """Fuel efficiency analysis"""
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.scatterplot(data=self.df.sample(min(500, len(self.df))), 
                       x='Engine_Load_percent', y='Fuel_Efficiency_Score',
                       hue='Type', ax=ax)
        ax.set_title("Fuel Efficiency vs Engine Load")
        self._save_plot(fig, "02_fuel_efficiency")
    
    def _plot_risk_distribution(self):
        """Risk assessment"""
        fig, ax = plt.subplots(figsize=(12, 6))
        self.df['Storm_Risk_Index'].hist(bins=30, ax=ax, edgecolor='black')
        ax.axvline(self.df['Storm_Risk_Index'].mean(), color='red', linestyle='--',
                  label=f"Mean: {self.df['Storm_Risk_Index'].mean():.1f}")
        ax.set_title("Storm Risk Index Distribution")
        ax.set_xlabel("Risk Index")
        ax.set_ylabel("Frequency")
        ax.legend()
        self._save_plot(fig, "03_risk_distribution")
    
    def _plot_engine_health(self):
        """Engine health by vessel type"""
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.violinplot(data=self.df, x='Type', y='Engine_Health_Score', ax=ax)
        ax.set_title("Engine Health Score by Vessel Type")
        self._save_plot(fig, "04_engine_health")
    
    def _plot_correlation(self):
        """Correlation matrix"""
        fig, ax = plt.subplots(figsize=(10, 8))
        cols = ['Speed_knots', 'Wave_Height_meters', 'Fuel_Efficiency_Score',
                'Engine_Load_percent', 'Storm_Risk_Index', 'Engine_Health_Score']
        corr = self.df[cols].corr()
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
        ax.set_title("Metrics Correlation Matrix")
        self._save_plot(fig, "05_correlation")
    
    def _save_plot(self, fig, filename):
        """Save plot"""
        path = os.path.join(self.output_dir, f"{filename}.png")
        fig.tight_layout()
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
    
    def generate_summary(self, metrics_df):
        """Generate summary statistics"""
        print("\n" + "="*70)
        print("SUMMARY STATISTICS")
        print("="*70)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        summary = self.df[numeric_cols].describe()
        
        stats_path = os.path.join(self.output_dir, 'summary_statistics.csv')
        summary.to_csv(stats_path)
        
        print(f"\nKey Metrics:")
        print(f"  Avg Speed: {self.df['Speed_knots'].mean():.2f} knots")
        print(f"  Avg Fuel Efficiency: {self.df['Fuel_Efficiency_Score'].mean():.1f}%")
        print(f"  Avg Engine Health: {self.df['Engine_Health_Score'].mean():.1f}%")
        print(f"  Avg Storm Risk: {self.df['Storm_Risk_Index'].mean():.1f}")
        print(f"  Total Maintenance Cost: ${self.df['Maintenance_Cost_USD'].sum():,.0f}")
        
        low_risk = len(metrics_df[metrics_df['composite_risk_score'] < 30])
        med_risk = len(metrics_df[(metrics_df['composite_risk_score'] >= 30) & 
                                 (metrics_df['composite_risk_score'] < 60)])
        high_risk = len(metrics_df[metrics_df['composite_risk_score'] >= 60])
        
        print(f"\nRisk Distribution:")
        print(f"  Low Risk: {low_risk} vessels")
        print(f"  Medium Risk: {med_risk} vessels")
        print(f"  High Risk: {high_risk} vessels")
        
        metrics_df = metrics_df.sort_values('composite_risk_score', ascending=False)
        metrics_path = os.path.join(self.output_dir, 'vessel_metrics.csv')
        metrics_df.to_csv(metrics_path)
        
        return metrics_df
