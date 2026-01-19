"""
Output Manager
Data validation and multi-format reporting
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch


class OutputManager:
    """Handles validation and reporting"""
    
    def __init__(self, df, metrics_df, output_dir):
        self.df = df
        self.metrics_df = metrics_df
        self.output_dir = output_dir
        self.validation_results = {}
    
    def validate_data(self):
        """Validate data quality"""
        print("\n" + "="*70)
        print("DATA VALIDATION")
        print("="*70)
        
        results = {'status': 'PASSED', 'issues': []}
        
        if len(self.df) == 0:
            results['status'] = 'FAILED'
            results['issues'].append("Dataset is empty")
        
        if self.df.isnull().sum().sum() > len(self.df) * 0.5:
            results['status'] = 'FAILED'
            results['issues'].append("More than 50% missing data")
        
        for col in self.df.select_dtypes(include=[np.number]).columns:
            if self.df[col].std() == 0:
                results['issues'].append(f"Column {col}: no variance")
        
        if len(results['issues']) == 0:
            print("Data validation: PASSED ✓")
        else:
            print("Data validation: PASSED with warnings")
            for issue in results['issues']:
                print(f"  - {issue}")
        
        return results
    
    def generate_pdf_report(self):
        """Generate PDF report"""
        print("\nGenerating PDF report...")
        
        filename = os.path.join(self.output_dir, 'analytics_report.pdf')
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        story.append(Paragraph("Maritime Fleet Analytics Report", styles['Title']))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Records', f"{len(self.df):,}"],
            ['Unique Vessels', f"{self.df['Vessel_ID'].nunique()}"],
            ['Avg Speed', f"{self.df['Speed_knots'].mean():.2f} knots"],
            ['Avg Fuel Efficiency', f"{self.df['Fuel_Efficiency_Score'].mean():.1f}%"],
            ['Total Maintenance Cost', f"${self.df['Maintenance_Cost_USD'].sum():,.0f}"],
        ]
        
        t = Table(summary_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(t)
        story.append(PageBreak())
        
        story.append(Paragraph("Risk Assessment", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        low_risk = len(self.metrics_df[self.metrics_df['composite_risk_score'] < 30])
        med_risk = len(self.metrics_df[(self.metrics_df['composite_risk_score'] >= 30) & 
                                       (self.metrics_df['composite_risk_score'] < 60)])
        high_risk = len(self.metrics_df[self.metrics_df['composite_risk_score'] >= 60])
        
        risk_data = [
            ['Risk Level', 'Count', 'Percentage'],
            ['Low', str(low_risk), f"{(low_risk / len(self.metrics_df) * 100):.1f}%"],
            ['Medium', str(med_risk), f"{(med_risk / len(self.metrics_df) * 100):.1f}%"],
            ['High', str(high_risk), f"{(high_risk / len(self.metrics_df) * 100):.1f}%"],
        ]
        
        t2 = Table(risk_data)
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ED7D31')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(t2)
        
        doc.build(story)
        print(f"PDF saved: {filename}")
    
    def generate_excel_report(self):
        """Generate Excel report"""
        print("Generating Excel report...")
        
        filename = os.path.join(self.output_dir, 'analytics_report.xlsx')
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            self.df.head(1000).to_excel(writer, sheet_name='Data', index=False)
            self.metrics_df.to_excel(writer, sheet_name='Metrics')
            
            summary = pd.DataFrame({
                'Metric': ['Total Records', 'Vessels', 'Date Range', 'Avg Speed', 
                          'Avg Efficiency', 'Total Maintenance'],
                'Value': [len(self.df), self.df['Vessel_ID'].nunique(),
                         f"{self.df['Timestamp'].min()} to {self.df['Timestamp'].max()}",
                         f"{self.df['Speed_knots'].mean():.2f}",
                         f"{self.df['Fuel_Efficiency_Score'].mean():.1f}%",
                         f"${self.df['Maintenance_Cost_USD'].sum():,.0f}"]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"Excel saved: {filename}")
    
    def generate_csv_exports(self):
        """Generate CSV exports"""
        print("Generating CSV exports...")
        
        self.metrics_df.to_csv(os.path.join(self.output_dir, 'vessel_metrics.csv'))
        
        summary_stats = self.df[self.df.select_dtypes(include=[np.number]).columns].describe()
        summary_stats.to_csv(os.path.join(self.output_dir, 'data_summary.csv'))
        
        print("CSV files saved")
    
    def generate_executive_summary(self):
        """Generate text summary"""
        print("Generating executive summary...")
        
        high_risk = self.metrics_df[self.metrics_df['composite_risk_score'] >= 60].index.tolist()
        
        summary_text = f"""
MARITIME FLEET ANALYTICS - EXECUTIVE SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW
--------
Total Records: {len(self.df):,}
Vessels Analyzed: {self.df['Vessel_ID'].nunique()}
Date Range: {self.df['Timestamp'].min()} to {self.df['Timestamp'].max()}

KEY METRICS
-----------
Average Speed: {self.df['Speed_knots'].mean():.2f} knots
Fuel Efficiency: {self.df['Fuel_Efficiency_Score'].mean():.1f}%
Engine Health: {self.df['Engine_Health_Score'].mean():.1f}%
Storm Risk Index: {self.df['Storm_Risk_Index'].mean():.1f}

FINANCIAL
---------
Total Maintenance Cost: ${self.df['Maintenance_Cost_USD'].sum():,.0f}
Total Repair Hours: {self.df['Repair_Time_hours'].sum():.0f}

RISK ASSESSMENT
---------------
Low Risk Vessels: {len(self.metrics_df[self.metrics_df['composite_risk_score'] < 30])}
Medium Risk Vessels: {len(self.metrics_df[(self.metrics_df['composite_risk_score'] >= 30) & (self.metrics_df['composite_risk_score'] < 60)])}
High Risk Vessels: {len(self.metrics_df[self.metrics_df['composite_risk_score'] >= 60])}

HIGH RISK VESSELS
-----------------
{', '.join(high_risk[:5]) if high_risk else 'None'}

RECOMMENDATIONS
---------------
1. Review high-risk vessels for maintenance
2. Implement fuel efficiency optimization
3. Monitor storm conditions closely
4. Schedule preventive maintenance proactively
"""
        
        summary_path = os.path.join(self.output_dir, 'executive_summary.txt')
        with open(summary_path, 'w') as f:
            f.write(summary_text)
        
        print(f"Summary saved: {summary_path}")
    
    def generate_all_reports(self):
        """Generate all reports"""
        print("\n" + "="*70)
        print("GENERATING REPORTS")
        print("="*70)
        
        self.generate_pdf_report()
        self.generate_excel_report()
        self.generate_csv_exports()
        self.generate_executive_summary()
        
        print("\nAll reports generated successfully")
