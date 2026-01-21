# Original Code by Vangara Yaswanth Sai 
# Built for Flipkart Task-4 Maritime Performance Analytics & Sea-Route Risk Assessment System for Ships/Submarines
# Task Given :- Build an end-to-end data analytics pipeline that integrates multiple marine datasets to analyze:
#Ship/submarine performance
#Fuel consumption & engine efficiency
#Sea-route risk levels
#Weather impact
#Navigation delays
#Maintenance patterns
#Ocean depth vs speed analysis
#This is a pure Data Science project (no machine learning required unless you want optional ML).
# Date(Last Updated): 17-01-2026  
"""
Maritime Analytics - Interactive Main Application
User-friendly CLI for data pipeline orchestration
"""

import os
import sys
import pandas as pd
from pathlib import Path
from core_data_pipeline import DataPipeline, select_data_source
from analytics_engine import AnalyticsEngine
from output_manager import OutputManager


class InteractiveApp:
    """Main application with interactive user interface"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.data_dir = self.project_dir / 'data'
        self.output_dir = self.project_dir / 'output'
        
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def display_banner(self):
        """Display welcome banner"""
        print("\n" + "="*70)
        print("MARITIME FLEET PERFORMANCE ANALYTICS")
        print("="*70)
        print("\nInteractive Data Analysis System")
        print("Analyze vessel performance, risks, and efficiency\n")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "-"*70)
        print("MAIN MENU")
        print("-"*70)
        print("1. Quick Analysis (Generate Data -> Analyze -> Report)")
        print("2. Load Your Own Data")
        print("3. Advanced Options")
        print("4. Launch Dashboard")
        print("5. Exit")
        print("-"*70)
    
    def quick_analysis(self):
        """Quick end-to-end analysis"""
        print("\n" + "="*70)
        print("QUICK ANALYSIS")
        print("="*70)
        
        num_vessels = self._get_integer_input(
            "Number of vessels to analyze (default 50): ", 50
        )
        num_records = self._get_integer_input(
            "Navigation records per vessel (default 100): ", 100
        )
        
        pipeline = DataPipeline(
            str(self.data_dir),
            num_vessels=num_vessels,
            nav_records=num_vessels * num_records
        )
        
        print("\nGenerating synthetic data...")
        pipeline.generate_synthetic_data()
        
        print("Integrating datasets...")
        integrated = pipeline.integrate_and_enrich()
        
        print("Analyzing data...")
        analytics = AnalyticsEngine(integrated, str(self.output_dir))
        metrics = analytics.calculate_all_metrics()
        
        num_charts = self._get_integer_input(
            "Number of visualizations (1-5, default 3): ", 3, max_val=5
        )
        analytics.generate_visualizations(num_charts)
        metrics_df = analytics.generate_summary(metrics)
        
        print("Generating reports...")
        output_mgr = OutputManager(integrated, metrics_df, str(self.output_dir))
        output_mgr.validate_data()
        output_mgr.generate_all_reports()
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print(f"\nOutputs saved to: {self.output_dir}")
        print("\nGenerated files:")
        print("  - analytics_report.pdf")
        print("  - analytics_report.xlsx")
        print("  - vessel_metrics.csv")
        print("  - executive_summary.txt")
        print("  - PNG visualizations (in output folder)")
    
    def load_user_data(self):
        """Load user-provided data"""
        print("\n" + "="*70)
        print("LOAD USER DATA")
        print("="*70)
        
        print("\nData source options:")
        print("1. Use default data/ folder (if CSV files exist)")
        print("2. Specify custom directory")
        print("3. Cancel")
        
        choice = input("\nChoice (1-3): ").strip()
        
        if choice == '1':
            data_source = str(self.data_dir)
        elif choice == '2':
            data_source = input("Enter full path to data directory: ").strip()
            if not os.path.isdir(data_source):
                print("Directory not found!")
                return
        else:
            return
        
        try:
            pipeline = DataPipeline(str(self.output_dir))
            
            print("\nLoading CSV files...")
            pipeline.load_user_data(data_source)
            
            print("Integrating data...")
            integrated = pipeline.integrate_and_enrich()
            
            print("Analyzing data...")
            analytics = AnalyticsEngine(integrated, str(self.output_dir))
            metrics = analytics.calculate_all_metrics()
            analytics.generate_visualizations(3)
            metrics_df = analytics.generate_summary(metrics)
            
            print("Generating reports...")
            output_mgr = OutputManager(integrated, metrics_df, str(self.output_dir))
            output_mgr.validate_data()
            output_mgr.generate_all_reports()
            
            print("\n" + "="*70)
            print("ANALYSIS COMPLETE")
            print("="*70)
        
        except Exception as e:
            print(f"\nError: {e}")
    
    def advanced_options(self):
        """Advanced configuration"""
        print("\n" + "="*70)
        print("ADVANCED OPTIONS")
        print("="*70)
        
        print("\n1. Custom data generation")
        print("2. Data validation only")
        print("3. Generate reports only")
        print("4. Back to main menu")
        
        choice = input("\nChoice (1-4): ").strip()
        
        if choice == '1':
            self._custom_generation()
        elif choice == '2':
            self._validation_only()
        elif choice == '3':
            self._reports_only()
    
    def _custom_generation(self):
        """Custom data generation"""
        print("\nCustom Data Generation")
        print("-"*40)
        
        num_vessels = self._get_integer_input("Number of vessels: ", 50, min_val=5, max_val=500)
        nav_records = self._get_integer_input("Total navigation records: ", 5000, min_val=100, max_val=100000)
        
        pipeline = DataPipeline(str(self.data_dir), num_vessels, nav_records)
        print("\nGenerating data...")
        pipeline.generate_synthetic_data()
        
        integrated = pipeline.integrate_and_enrich()
        print(f"Generated {len(integrated)} integrated records")
        print("Data saved to: data/")
    
    def _validation_only(self):
        """Validate existing data"""
        print("\nData Validation")
        print("-"*40)
        
        try:
            csv_path = os.path.join(self.data_dir, 'integrated_data.csv')
            if not os.path.exists(csv_path):
                print("No integrated data found. Run analysis first.")
                return
            
            df = pd.read_csv(csv_path)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            
            output_mgr = OutputManager(df, None, str(self.output_dir))
            output_mgr.validate_data()
        
        except Exception as e:
            print(f"Error: {e}")
    
    def _reports_only(self):
        """Generate reports from existing data"""
        print("\nReport Generation")
        print("-"*40)
        
        try:
            import pandas as pd
            
            csv_path = os.path.join(self.data_dir, 'integrated_data.csv')
            metrics_path = os.path.join(self.output_dir, 'vessel_metrics.csv')
            
            if not os.path.exists(csv_path):
                print("No integrated data found.")
                return
            
            df = pd.read_csv(csv_path)
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            
            metrics_df = pd.read_csv(metrics_path, index_col=0) if os.path.exists(metrics_path) else None
            
            output_mgr = OutputManager(df, metrics_df, str(self.output_dir))
            output_mgr.generate_all_reports()
            
            print("Reports generated successfully")
        
        except Exception as e:
            print(f"Error: {e}")
    
    def launch_dashboard(self):
        """Launch Streamlit dashboard"""
        print("\n" + "="*70)
        print("LAUNCHING DASHBOARD")
        print("="*70)
        
        dashboard_path = self.project_dir / 'streamlit_dashboard.py'
        
        if not dashboard_path.exists():
            print("Dashboard not found!")
            return
        
        print("\nStarting Streamlit dashboard...")
        print("(Browser will open automatically)\n")
        
        os.system(f'streamlit run "{dashboard_path}"')
    
    def _get_integer_input(self, prompt, default, min_val=1, max_val=None):
        """Get validated integer input"""
        while True:
            try:
                value = input(prompt).strip()
                if not value:
                    return default
                
                num = int(value)
                if num < min_val:
                    print(f"Value must be >= {min_val}")
                    continue
                if max_val and num > max_val:
                    print(f"Value must be <= {max_val}")
                    continue
                
                return num
            except ValueError:
                print("Please enter a valid number")
    
    def run(self):
        """Main application loop"""
        self.display_banner()
        
        while True:
            self.display_menu()
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == '1':
                self.quick_analysis()
            elif choice == '2':
                self.load_user_data()
            elif choice == '3':
                self.advanced_options()
            elif choice == '4':
                self.launch_dashboard()
            elif choice == '5':
                print("\nExiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")


def main():
    """Entry point"""
    try:
        import pandas as pd
        import numpy as np
    except ImportError:
        print("Error: Required packages not installed")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    app = InteractiveApp()
    app.run()


if __name__ == "__main__":
    main()
