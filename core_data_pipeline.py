"""
Data Pipeline
Generates synthetic data or loads user data, then integrates everything
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta


class DataPipeline:
    """Unified data generation and integration"""
    
    def __init__(self, output_dir, num_vessels=50, nav_records=5000):
        self.output_dir = output_dir
        self.num_vessels = num_vessels
        self.nav_records = nav_records
        self.data = {}
        self.integrated_data = None
        np.random.seed(42)
    
    @property
    def df(self):
        """Alias for integrated_data"""
        return self.integrated_data
    
    def generate_synthetic_data(self):
        """Generate all 5 synthetic datasets"""
        print("\n" + "="*70)
        print("GENERATING SYNTHETIC DATA")
        print("="*70)
        
        self.data['vessels'] = self._generate_vessels()
        print(f"Generated {len(self.data['vessels'])} vessel specifications")
        
        self.data['navigation'] = self._generate_navigation()
        print(f"Generated {len(self.data['navigation'])} navigation records")
        
        self.data['environment'] = self._generate_environment()
        print(f"Generated {len(self.data['environment'])} environmental records")
        
        self.data['fuel'] = self._generate_fuel()
        print(f"Generated {len(self.data['fuel'])} fuel records")
        
        self.data['maintenance'] = self._generate_maintenance()
        print(f"Generated {len(self.data['maintenance'])} maintenance records")
        
        return self.data
    
    def load_user_data(self, data_dir):
        """Load user-provided CSV files"""
        print("\n" + "="*70)
        print("LOADING USER DATA")
        print("="*70)
        
        required_files = {
            'vessels': 'vessel_specifications.csv',
            'navigation': 'navigation_logs.csv',
            'environment': 'environmental_conditions.csv',
            'fuel': 'fuel_consumption.csv',
            'maintenance': 'maintenance_incidents.csv'
        }
        
        loaded = 0
        for key, filename in required_files.items():
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                self.data[key] = pd.read_csv(filepath)
                print(f"Loaded {filename}: {len(self.data[key])} records")
                loaded += 1
            else:
                print(f"Warning: {filename} not found")
        
        if loaded == 0:
            raise FileNotFoundError("No data files found. Generate synthetic data or provide CSV files.")
        
        return self.data
    
    def _generate_vessels(self):
        """Generate vessel specifications"""
        vessel_types = ['Cargo', 'Naval', 'Submarine', 'Tanker', 'Passenger']
        fuel_types = ['Heavy Fuel Oil', 'Marine Diesel', 'LNG', 'Nuclear']
        
        data = []
        for i in range(self.num_vessels):
            data.append({
                'Vessel_ID': f"V{i+1:03d}",
                'Type': np.random.choice(vessel_types),
                'Engine_Power_kW': np.random.randint(5000, 50000),
                'Fuel_Type': np.random.choice(fuel_types),
                'Max_Depth_meters': np.random.randint(100, 3000),
                'Load_Capacity_tons': np.random.randint(5000, 50000),
                'Length_meters': np.random.uniform(50, 300),
                'Year_Built': np.random.randint(2000, 2023)
            })
        
        return pd.DataFrame(data)
    
    def _generate_navigation(self):
        """Generate navigation logs"""
        data = []
        start_time = datetime.now() - timedelta(days=30)
        
        for vessel in self.data['vessels']['Vessel_ID'].unique():
            for i in range(self.nav_records // self.num_vessels):
                timestamp = start_time + timedelta(hours=i)
                data.append({
                    'Vessel_ID': vessel,
                    'Timestamp': timestamp,
                    'Latitude': np.random.uniform(-90, 90),
                    'Longitude': np.random.uniform(-180, 180),
                    'Speed_knots': np.random.uniform(0, 25),
                    'Engine_RPM': np.random.randint(100, 3000),
                    'Depth_meters': np.random.uniform(0, 5000),
                    'Distance_covered_nm': np.random.uniform(1, 50),
                    'Course_Deviation_degrees': np.random.uniform(-30, 30)
                })
        
        return pd.DataFrame(data)
    
    def _generate_environment(self):
        """Generate environmental conditions"""
        data = []
        start_time = datetime.now() - timedelta(days=30)
        
        for i in range(self.nav_records // 10):
            timestamp = start_time + timedelta(hours=i*4)
            data.append({
                'Timestamp': timestamp,
                'Wave_Height_meters': np.random.exponential(1.5),
                'Wind_Speed_knots': np.random.gamma(2, 2),
                'Visibility_km': np.random.uniform(0.5, 20),
                'Sea_Temperature_C': np.random.uniform(-2, 30),
                'Ocean_Current_knots': np.random.uniform(0, 3),
                'Storm_Probability_percent': np.random.uniform(0, 100)
            })
        
        return pd.DataFrame(data)
    
    def _generate_fuel(self):
        """Generate fuel consumption logs"""
        data = []
        start_time = datetime.now() - timedelta(days=30)
        
        for vessel in self.data['vessels']['Vessel_ID'].unique():
            for i in range(self.nav_records // self.num_vessels):
                timestamp = start_time + timedelta(hours=i)
                data.append({
                    'Vessel_ID': vessel,
                    'Timestamp': timestamp,
                    'Fuel_Used_per_Hour_liters': np.random.uniform(50, 5000),
                    'Fuel_Used_per_NM_liters': np.random.uniform(1, 100),
                    'Fuel_Cost_USD': np.random.uniform(100, 10000),
                    'Load_Weight_percent': np.random.uniform(0, 100),
                    'Engine_Load_percent': np.random.uniform(20, 100)
                })
        
        return pd.DataFrame(data)
    
    def _generate_maintenance(self):
        """Generate maintenance incidents"""
        data = []
        start_time = datetime.now() - timedelta(days=30)
        maintenance_types = ['Engine Overhaul', 'Hull Inspection', 'Propulsion Repair', 
                            'Electrical System', 'Navigation Equipment']
        risk_categories = ['Low', 'Medium', 'High']
        incident_types = ['Mechanical Failure', 'Preventive', 'Inspection', 'Emergency']
        
        for vessel in self.data['vessels']['Vessel_ID'].unique():
            num_incidents = np.random.randint(1, 10)
            for i in range(num_incidents):
                timestamp = start_time + timedelta(days=np.random.randint(0, 30))
                data.append({
                    'Vessel_ID': vessel,
                    'Timestamp': timestamp,
                    'Maintenance_Type': np.random.choice(maintenance_types),
                    'Repair_Time_hours': np.random.uniform(1, 72),
                    'Maintenance_Cost_USD': np.random.uniform(5000, 50000),
                    'Risk_Category': np.random.choice(risk_categories),
                    'Incident_Type': np.random.choice(incident_types)
                })
        
        return pd.DataFrame(data)
    
    def integrate_and_enrich(self):
        """Merge all datasets and calculate derived metrics"""
        print("\n" + "="*70)
        print("INTEGRATING DATA")
        print("="*70)
        
        df_nav = self.data['navigation'].copy()
        df_nav['Timestamp'] = pd.to_datetime(df_nav['Timestamp'])
        df_nav['Hour'] = df_nav['Timestamp'].dt.floor('h')
        
        df_env = self.data['environment'].copy()
        df_env['Timestamp'] = pd.to_datetime(df_env['Timestamp'])
        df_env['Hour'] = pd.to_datetime(df_env['Timestamp']).dt.floor('h')
        
        merged = df_nav.merge(df_env, on='Hour', how='left').bfill()
        
        df_fuel = self.data['fuel'].copy()
        df_fuel['Timestamp'] = pd.to_datetime(df_fuel['Timestamp'])
        df_fuel['Date'] = df_fuel['Timestamp'].dt.date
        
        # Keep Timestamp from navigation for later use
        if 'Timestamp_x' in merged.columns:
            merged['Timestamp'] = merged['Timestamp_x']
        elif 'Timestamp' not in merged.columns:
            merged['Timestamp'] = merged['Timestamp_y'] if 'Timestamp_y' in merged.columns else df_nav['Timestamp'].values[0]
        
        merged['Date'] = pd.to_datetime(merged['Timestamp']).dt.date
        
        merged = merged.merge(
            df_fuel[['Vessel_ID', 'Date', 'Fuel_Used_per_Hour_liters', 
                     'Fuel_Used_per_NM_liters', 'Fuel_Cost_USD', 
                     'Load_Weight_percent', 'Engine_Load_percent']],
            on=['Vessel_ID', 'Date'], how='left'
        )
        
        merged = merged.merge(
            self.data['vessels'],
            on='Vessel_ID', how='left'
        )
        
        df_maint = self.data['maintenance'].copy()
        df_maint['Timestamp'] = pd.to_datetime(df_maint['Timestamp'])
        df_maint_daily = df_maint.groupby(['Vessel_ID', df_maint['Timestamp'].dt.date]).agg({
            'Maintenance_Type': lambda x: ', '.join(x.unique()),
            'Repair_Time_hours': 'sum',
            'Maintenance_Cost_USD': 'sum',
            'Risk_Category': lambda x: x.value_counts().index[0] if len(x) > 0 else 'Low',
        }).reset_index()
        
        df_maint_daily.rename(columns={'Timestamp': 'Date'}, inplace=True)
        merged = merged.merge(df_maint_daily, on=['Vessel_ID', 'Date'], how='left')
        merged['Repair_Time_hours'] = merged['Repair_Time_hours'].fillna(0)
        merged['Maintenance_Cost_USD'] = merged['Maintenance_Cost_USD'].fillna(0)
        
        self._calculate_metrics(merged)
        
        merged = merged.drop(['Hour', 'Date'], errors='ignore', axis=1)
        merged = merged.drop_duplicates(subset=['Vessel_ID', 'Timestamp'], keep='first')
        merged = merged.sort_values(['Vessel_ID', 'Timestamp']).reset_index(drop=True)
        
        self.integrated_data = merged
        
        output_path = os.path.join(self.output_dir, 'integrated_data.csv')
        merged.to_csv(output_path, index=False)
        print(f"Integrated data saved: {output_path}")
        
        return merged
    
    def _calculate_metrics(self, df):
        """Calculate derived metrics"""
        df['NM_per_Liter'] = np.where(
            (df['Fuel_Used_per_NM_liters'] > 0) & (df['Distance_covered_nm'] > 0),
            df['Distance_covered_nm'] / df['Fuel_Used_per_NM_liters'], 0
        )
        
        max_nm = df[df['NM_per_Liter'] > 0]['NM_per_Liter'].quantile(0.95)
        df['Fuel_Efficiency_Score'] = np.where(
            df['NM_per_Liter'] > 0,
            np.clip((df['NM_per_Liter'] / max_nm * 100), 0, 100), 50
        )
        
        df['Vessel_Utilization_Rate'] = (
            df['Load_Weight_percent'].fillna(50) * 0.6 +
            (df['Speed_knots'].fillna(0) / 25 * 100) * 0.4
        ).clip(0, 100)
        
        df['Storm_Risk_Index'] = np.clip(
            df['Storm_Probability_percent'].fillna(0) * 0.5 +
            (df['Wave_Height_meters'].fillna(0) / 6) * 50, 0, 100
        )
        
        df['Engine_Health_Score'] = np.where(
            df['Engine_RPM'] > 0,
            np.clip(100 - (df['Engine_Load_percent'].fillna(50) * 0.4 +
                           df['Maintenance_Cost_USD'].fillna(0) / 100 * 0.3 +
                           df['Repair_Time_hours'].fillna(0) * 0.5), 20, 100), 75
        )
        
        df['Navigation_Difficulty'] = np.clip(
            df['Wave_Height_meters'].fillna(0) * 10 +
            df['Wind_Speed_knots'].fillna(0) * 2 +
            (100 - df['Visibility_km'].fillna(10) * 5), 0, 100
        )


def select_data_source():
    """Interactive data source selection"""
    print("\n" + "="*70)
    print("DATA SOURCE SELECTION")
    print("="*70)
    print("\nChoose data source:")
    print("1. Generate synthetic data")
    print("2. Load from CSV files")
    print("3. Load from custom directory")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    return choice
