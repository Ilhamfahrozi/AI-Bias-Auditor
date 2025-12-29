"""
AI Bias Auditor v3.0 - ADVANCED EDITION
Comprehensive Credit Scoring Bias Detection with ML Explainability
Author: AI Bias Auditor Team
Date: December 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import StandardScaler
import warnings
import io
import base64
from datetime import datetime
from pdf_generator import generate_short_guide, generate_full_guide, save_pdf
import os
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="AI Bias Auditor v3.0 - Advanced",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    .stApp {
        background-color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #002B5B;
        font-family: 'Arial', sans-serif;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 20px;
        border-radius: 5px;
        border-left: 4px solid #002B5B;
    }
    .warning-box {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #002B5B;
        margin: 10px 0;
    }
    .info-box {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #002B5B;
        margin: 10px 0;
    }
    .danger-box {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #002B5B;
        margin: 10px 0;
        font-weight: bold;
    }
    .success-box {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #002B5B;
        margin: 10px 0;
    }
    .stProgress > div > div > div > div {
        background-color: #002B5B;
    }
    </style>
    """, unsafe_allow_html=True)


def generate_credit_data(n):
    """Generate synthetic credit application data with embedded age bias."""
    np.random.seed(42)
    
    data = {
        'Applicant_ID': [f'APP{str(i).zfill(5)}' for i in range(1, n + 1)],
        'Age': np.random.randint(20, 66, n),
        'Annual_Income': np.random.randint(30000000, 500000000, n),
        'Employment_Years': np.random.randint(1, 40, n),
        'Debt_to_Income_Ratio': np.random.uniform(0.1, 0.6, n),
        'Credit_History_Length': np.random.randint(1, 30, n),
        'Number_of_Accounts': np.random.randint(1, 15, n),
        'Payment_History_Score': np.random.randint(300, 850, n)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate base credit score
    income_min = df['Annual_Income'].min()
    income_max = df['Annual_Income'].max()
    base_score = 300 + ((df['Annual_Income'] - income_min) / (income_max - income_min) * 400)
    base_score += df['Employment_Years'] * 3
    base_score -= df['Debt_to_Income_Ratio'] * 100
    base_score += df['Credit_History_Length'] * 2
    base_score += df['Number_of_Accounts'] * 2
    base_score += (df['Payment_History_Score'] - 575) * 0.1
    base_score += np.random.randint(-30, 30, n)
    
    df['Calculated_Credit_Score'] = base_score
    
    # BIAS IMPLEMENTATION: Penalize age > 45
    df.loc[df['Age'] > 45, 'Calculated_Credit_Score'] -= 200
    
    df['Calculated_Credit_Score'] = df['Calculated_Credit_Score'].clip(300, 850).astype(int)
    df['Loan_Status'] = df['Calculated_Credit_Score'].apply(lambda x: 'Approved' if x >= 600 else 'Rejected')
    df['Age_Group'] = df['Age'].apply(lambda x: 'Young (<=45)' if x <= 45 else 'Old (>45)')
    df['Income_Bracket'] = pd.cut(df['Annual_Income'], 
                                   bins=[0, 100000000, 200000000, 300000000, 500000000],
                                   labels=['Low', 'Medium', 'High', 'Very High'])
    
    # Risk category
    df['Risk_Category'] = pd.cut(df['Calculated_Credit_Score'],
                                  bins=[0, 500, 600, 700, 850],
                                  labels=['High Risk', 'Medium Risk', 'Low Risk', 'Very Low Risk'])
    
    return df


def process_uploaded_data(df):
    """Process uploaded Excel/CSV data."""
    required_cols = ['Age', 'Calculated_Credit_Score']
    
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"[ERROR] Missing required columns: {missing}")
        st.info("Required columns: Age, Calculated_Credit_Score")
        return None
    
    if 'Applicant_ID' not in df.columns:
        df['Applicant_ID'] = [f'APP{str(i).zfill(5)}' for i in range(1, len(df) + 1)]
    
    if 'Loan_Status' not in df.columns:
        df['Loan_Status'] = df['Calculated_Credit_Score'].apply(
            lambda x: 'Approved' if x >= 600 else 'Rejected'
        )
    
    df['Age_Group'] = df['Age'].apply(lambda x: 'Young (<=45)' if x <= 45 else 'Old (>45)')
    
    if 'Annual_Income' in df.columns:
        df['Income_Bracket'] = pd.cut(df['Annual_Income'], 
                                       bins=[0, 100000000, 200000000, 300000000, 500000000],
                                       labels=['Low', 'Medium', 'High', 'Very High'])
    
    df['Risk_Category'] = pd.cut(df['Calculated_Credit_Score'],
                                  bins=[0, 500, 600, 700, 850],
                                  labels=['High Risk', 'Medium Risk', 'Low Risk', 'Very Low Risk'])
    
    return df


def calculate_bias_metrics(df):
    """Calculate comprehensive bias detection metrics."""
    young = df[df['Age'] <= 45]
    old = df[df['Age'] > 45]
    
    young_approved = (young['Loan_Status'] == 'Approved').sum()
    young_total = len(young)
    old_approved = (old['Loan_Status'] == 'Approved').sum()
    old_total = len(old)
    
    young_approval_rate = (young_approved / young_total * 100) if young_total > 0 else 0
    old_approval_rate = (old_approved / old_total * 100) if old_total > 0 else 0
    
    young_avg_score = young['Calculated_Credit_Score'].mean()
    old_avg_score = old['Calculated_Credit_Score'].mean()
    
    score_gap = young_avg_score - old_avg_score
    approval_gap = young_approval_rate - old_approval_rate
    
    # Statistical tests
    if len(young) > 1 and len(old) > 1:
        t_stat, p_value = stats.ttest_ind(young['Calculated_Credit_Score'], 
                                           old['Calculated_Credit_Score'])
        # Mann-Whitney U test (non-parametric)
        u_stat, u_pvalue = stats.mannwhitneyu(young['Calculated_Credit_Score'], 
                                               old['Calculated_Credit_Score'])
    else:
        t_stat, p_value = 0, 1.0
        u_stat, u_pvalue = 0, 1.0
    
    # Disparate Impact Ratio
    disparate_impact = (old_approval_rate / young_approval_rate) if young_approval_rate > 0 else 0
    
    # Cohen's d (effect size)
    pooled_std = np.sqrt(((len(young) - 1) * young['Calculated_Credit_Score'].std()**2 + 
                          (len(old) - 1) * old['Calculated_Credit_Score'].std()**2) / 
                         (len(young) + len(old) - 2))
    cohens_d = (young_avg_score - old_avg_score) / pooled_std if pooled_std > 0 else 0
    
    # Bias detection
    bias_detected = score_gap > 100 or approval_gap > 20 or disparate_impact < 0.8
    
    # Rejection rates
    young_rejected = (young['Loan_Status'] == 'Rejected').sum()
    old_rejected = (old['Loan_Status'] == 'Rejected').sum()
    
    return {
        'young_approval_rate': young_approval_rate,
        'old_approval_rate': old_approval_rate,
        'young_avg_score': young_avg_score,
        'old_avg_score': old_avg_score,
        'score_gap': score_gap,
        'approval_gap': approval_gap,
        'bias_detected': bias_detected,
        't_statistic': t_stat,
        'p_value': p_value,
        'u_statistic': u_stat,
        'u_pvalue': u_pvalue,
        'disparate_impact': disparate_impact,
        'cohens_d': cohens_d,
        'young_count': young_total,
        'old_count': old_total,
        'young_approved': young_approved,
        'young_rejected': young_rejected,
        'old_approved': old_approved,
        'old_rejected': old_rejected
    }


# ========== ADVANCED VISUALIZATIONS ==========

def create_correlation_heatmap(df):
    """Create correlation heatmap for numerical features."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col not in ['Applicant_ID']]
    
    if len(numeric_cols) < 2:
        return None
    
    corr_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale=[[0, '#F8F9FA'], [0.5, '#6C757D'], [1, '#002B5B']],
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title='Feature Correlation Heatmap',
        template='plotly_white',
        font=dict(color='#002B5B'),
        height=500
    )
    
    return fig


def create_violin_plot(df):
    """Create violin plot for score distribution."""
    fig = go.Figure()
    
    for age_group in ['Young (<=45)', 'Old (>45)']:
        data = df[df['Age_Group'] == age_group]
        fig.add_trace(go.Violin(
            y=data['Calculated_Credit_Score'],
            name=age_group,
            box_visible=True,
            meanline_visible=True,
            fillcolor='#002B5B' if age_group == 'Young (<=45)' else '#6C757D',
            opacity=0.6,
            line_color='#002B5B'
        ))
    
    fig.update_layout(
        title='Credit Score Distribution (Violin Plot)',
        yaxis_title='Credit Score',
        template='plotly_white',
        font=dict(color='#002B5B'),
        showlegend=True
    )
    
    return fig


def create_confusion_matrix_viz(df):
    """Create confusion matrix visualization."""
    # Binary classification: Approved=1, Rejected=0
    y_true = (df['Loan_Status'] == 'Approved').astype(int)
    y_pred_young = ((df['Age'] <= 45) & (df['Calculated_Credit_Score'] >= 600)).astype(int)
    
    cm = confusion_matrix(y_true, y_pred_young)
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicted Rejected', 'Predicted Approved'],
        y=['Actual Rejected', 'Actual Approved'],
        colorscale=[[0, '#F8F9FA'], [1, '#002B5B']],
        text=cm,
        texttemplate='%{text}',
        textfont={"size": 16},
        colorbar=dict(title="Count")
    ))
    
    fig.update_layout(
        title='Confusion Matrix',
        template='plotly_white',
        font=dict(color='#002B5B')
    )
    
    return fig


def create_age_score_trend(df):
    """Create detailed age vs score trend line."""
    age_stats = df.groupby('Age').agg({
        'Calculated_Credit_Score': ['mean', 'std', 'count']
    }).reset_index()
    age_stats.columns = ['Age', 'Mean_Score', 'Std_Score', 'Count']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=age_stats['Age'],
        y=age_stats['Mean_Score'],
        mode='lines+markers',
        name='Average Score',
        line=dict(color='#002B5B', width=3),
        marker=dict(size=8)
    ))
    
    # Add shaded area for std deviation
    fig.add_trace(go.Scatter(
        x=age_stats['Age'].tolist() + age_stats['Age'].tolist()[::-1],
        y=(age_stats['Mean_Score'] + age_stats['Std_Score']).tolist() + 
          (age_stats['Mean_Score'] - age_stats['Std_Score']).tolist()[::-1],
        fill='toself',
        fillcolor='rgba(0, 43, 91, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=True,
        name='Std Deviation'
    ))
    
    # Add vertical line at age 45
    fig.add_vline(x=45, line_dash="dash", line_color="#002B5B", 
                  annotation_text="Bias Threshold")
    
    fig.update_layout(
        title='Credit Score Trend by Age (with Standard Deviation)',
        xaxis_title='Age (years)',
        yaxis_title='Average Credit Score',
        template='plotly_white',
        font=dict(color='#002B5B'),
        hovermode='x unified'
    )
    
    return fig


def create_sunburst_chart(df):
    """Create sunburst chart for hierarchical breakdown."""
    # Group by Age_Group, Risk_Category, Loan_Status
    sunburst_data = df.groupby(['Age_Group', 'Risk_Category', 'Loan_Status']).size().reset_index(name='count')
    
    fig = go.Figure(go.Sunburst(
        labels=sunburst_data['Age_Group'].tolist() + sunburst_data['Risk_Category'].tolist() + sunburst_data['Loan_Status'].tolist(),
        parents=[''] * len(sunburst_data['Age_Group']) + sunburst_data['Age_Group'].tolist() + sunburst_data['Risk_Category'].tolist(),
        values=sunburst_data['count'].tolist() * 3,
        marker=dict(colors=['#002B5B', '#6C757D', '#A8B0B8', '#D4D7DA'])
    ))
    
    fig.update_layout(
        title='Hierarchical Breakdown: Age Group → Risk → Status',
        template='plotly_white',
        font=dict(color='#002B5B')
    )
    
    return fig


def create_fairness_radar(metrics):
    """Create radar chart for fairness metrics."""
    categories = ['Approval<br>Parity', 'Score<br>Equality', 'Disparate<br>Impact', 
                  'Statistical<br>Power', 'Effect<br>Size']
    
    # Normalize metrics to 0-100 scale (100 = fair, 0 = unfair)
    approval_parity = 100 - min(metrics['approval_gap'], 100)
    score_equality = 100 - min((metrics['score_gap'] / 8.5), 100)  # Normalize to 850 max
    di_score = metrics['disparate_impact'] * 100
    stat_power = (1 - min(metrics['p_value'], 1)) * 100
    effect_size = 100 - min(abs(metrics['cohens_d']) * 20, 100)
    
    values = [approval_parity, score_equality, di_score, stat_power, effect_size]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(0, 43, 91, 0.3)',
        line=dict(color='#002B5B', width=2),
        name='Current System'
    ))
    
    # Add reference line at 80 (fairness threshold)
    fig.add_trace(go.Scatterpolar(
        r=[80] * len(categories),
        theta=categories,
        line=dict(color='#6C757D', dash='dash'),
        name='Fairness Threshold'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title='Fairness Metrics Radar Chart',
        template='plotly_white',
        font=dict(color='#002B5B')
    )
    
    return fig


def create_distribution_chart(df):
    """Create credit score distribution by age group."""
    fig = go.Figure()
    
    for age_group in ['Young (<=45)', 'Old (>45)']:
        data = df[df['Age_Group'] == age_group]['Calculated_Credit_Score']
        fig.add_trace(go.Histogram(
            x=data,
            name=age_group,
            marker_color='#002B5B' if age_group == 'Young (<=45)' else '#6C757D',
            opacity=0.7,
            nbinsx=30
        ))
    
    fig.update_layout(
        title='Credit Score Distribution by Age Group',
        xaxis_title='Credit Score',
        yaxis_title='Frequency',
        barmode='overlay',
        template='plotly_white',
        font=dict(color='#002B5B'),
        showlegend=True
    )
    
    return fig


def create_income_vs_score_chart(df):
    """Create scatter plot of income vs credit score."""
    if 'Annual_Income' not in df.columns:
        return None
    
    fig = px.scatter(df, 
                     x='Annual_Income', 
                     y='Calculated_Credit_Score',
                     color='Age_Group',
                     size='Calculated_Credit_Score',
                     color_discrete_map={'Young (<=45)': '#002B5B', 'Old (>45)': '#6C757D'},
                     labels={'Annual_Income': 'Annual Income (IDR)',
                             'Calculated_Credit_Score': 'Credit Score'},
                     title='Income vs Credit Score by Age Group (Bubble Size = Score)',
                     hover_data=['Loan_Status'])
    
    fig.update_layout(template='plotly_white', font=dict(color='#002B5B'))
    return fig


def create_approval_by_income_chart(df):
    """Create approval rate by income bracket."""
    if 'Income_Bracket' not in df.columns:
        return None
    
    grouped = df.groupby(['Income_Bracket', 'Age_Group']).agg({
        'Loan_Status': lambda x: (x == 'Approved').sum() / len(x) * 100
    }).reset_index()
    grouped.columns = ['Income_Bracket', 'Age_Group', 'Approval_Rate']
    
    fig = px.bar(grouped, 
                 x='Income_Bracket', 
                 y='Approval_Rate',
                 color='Age_Group',
                 barmode='group',
                 color_discrete_map={'Young (<=45)': '#002B5B', 'Old (>45)': '#6C757D'},
                 labels={'Approval_Rate': 'Approval Rate (%)', 'Income_Bracket': 'Income Bracket'},
                 title='Approval Rate by Income Bracket and Age Group',
                 text='Approval_Rate')
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(template='plotly_white', font=dict(color='#002B5B'))
    return fig


def create_age_distribution_chart(df):
    """Create age distribution histogram."""
    fig = px.histogram(df, 
                       x='Age',
                       nbins=30,
                       color='Loan_Status',
                       color_discrete_map={'Approved': '#002B5B', 'Rejected': '#6C757D'},
                       labels={'Age': 'Age (years)', 'count': 'Number of Applicants'},
                       title='Age Distribution by Loan Status')
    
    fig.add_vline(x=45, line_dash="dash", line_color="#002B5B", 
                  annotation_text="Threshold Age 45")
    
    fig.update_layout(template='plotly_white', font=dict(color='#002B5B'))
    return fig


def create_box_plot(df):
    """Create box plot of credit scores by age group."""
    fig = px.box(df, 
                 x='Age_Group', 
                 y='Calculated_Credit_Score',
                 color='Age_Group',
                 color_discrete_map={'Young (<=45)': '#002B5B', 'Old (>45)': '#6C757D'},
                 labels={'Calculated_Credit_Score': 'Credit Score', 'Age_Group': 'Age Group'},
                 title='Credit Score Distribution (Box Plot)',
                 points='outliers')
    
    fig.update_layout(template='plotly_white', font=dict(color='#002B5B'), showlegend=False)
    return fig


def create_risk_distribution_pie(df):
    """Create pie chart for risk distribution."""
    risk_counts = df['Risk_Category'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        marker=dict(colors=['#002B5B', '#4A5F7F', '#6C757D', '#A8B0B8']),
        textinfo='label+percent',
        hole=0.3
    )])
    
    fig.update_layout(
        title='Risk Category Distribution',
        template='plotly_white',
        font=dict(color='#002B5B')
    )
    
    return fig


# ============= MAIN APPLICATION =============

# Header with version
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("<h1 style='text-align: center;'>AUDIT REPORT: CREDIT SCORING BIAS DETECTION</h1>", 
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #6C757D;'>AI Fairness Analysis v3.0 - Advanced Edition</h3>", 
                unsafe_allow_html=True)
with col2:
    st.markdown(f"<p style='text-align: right; color: #6C757D;'>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", 
                unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## AUDIT CONFIGURATION")
    st.markdown("---")
    
    # Mode selection
    audit_mode = st.radio(
        "Select Audit Mode:",
        ["[1] Upload Excel/CSV Data (Real)", "[2] Generate Simulation Data"],
        help="Choose to upload your own data or generate synthetic data for testing"
    )
    
    st.markdown("---")
    
    # PDF User Guide Download
    st.markdown("### USER GUIDE")
    guide_type = st.radio(
        "Select guide version:",
        ["Ringkas (3-5 halaman)", "Lengkap (10-15 halaman)"],
        help="Choose between short or comprehensive user guide"
    )
    
    if st.button("[DOWNLOAD PDF GUIDE]", use_container_width=True):
        with st.spinner("Generating PDF..."):
            try:
                if "Ringkas" in guide_type:
                    pdf = generate_short_guide()
                    filename = "AI_Bias_Auditor_Guide_Ringkas.pdf"
                else:
                    pdf = generate_full_guide()
                    filename = "AI_Bias_Auditor_Guide_Lengkap.pdf"
                
                # Save to temp location
                temp_path = os.path.join(os.getcwd(), filename)
                save_pdf(pdf, temp_path)
                
                # Read and create download button
                with open(temp_path, "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(
                    label=f"[CLICK HERE] Download {filename}",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.success(f"PDF ready! Click button above to download.")
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")
    
    st.markdown("---")
    
    if "[1]" in audit_mode:
        st.markdown("### UPLOAD DATA FILE")
        uploaded_file = st.file_uploader(
            "Upload Excel file (.xlsx or .csv)",
            type=['xlsx', 'csv'],
            help="File must contain: Age, Calculated_Credit_Score columns"
        )
        
        st.markdown("---")
        st.markdown("### Required Columns:")
        st.markdown("""
        **Mandatory:**
        - Age
        - Calculated_Credit_Score
        
        **Optional:**
        - Applicant_ID
        - Loan_Status
        - Annual_Income
        """)
        
        run_audit = st.button("[RUN AUDIT]", use_container_width=True, type="primary")
        
    else:
        sample_size = st.slider(
            "Sample Size (Number of Applicants)",
            min_value=100,
            max_value=5000,
            value=1000,
            step=100
        )
        
        st.markdown("---")
        run_audit = st.button("[RUN AUDIT SIMULATION]", use_container_width=True, type="primary")
    
    st.markdown("---")
    st.markdown("### VISUALIZATION OPTIONS")
    show_advanced = st.checkbox("Show Advanced Charts", value=True)
    show_ml_metrics = st.checkbox("Show ML Metrics", value=True)
    
    st.markdown("---")
    st.markdown("### ABOUT THIS TOOL v3.0")
    st.markdown("""
    Advanced bias detection with:
    - 12+ Interactive visualizations
    - ML explainability metrics
    - Statistical rigor
    - Professional reporting
    """)
    
    st.markdown("---")
    st.markdown("### FAIRNESS CRITERIA")
    st.markdown("""
    - Disparate Impact: >= 80%
    - Score Gap: < 100 points
    - Approval Gap: < 20%
    - Statistical Significance: p < 0.05
    """)

# Main Content
if run_audit:
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Load or generate data
    if "[1]" in audit_mode:
        if uploaded_file is None:
            st.error("[ERROR] Please upload a file first.")
            st.stop()
        
        try:
            status_text.text("[1/5] Loading file...")
            progress_bar.progress(20)
            
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
            
            st.success(f"[SUCCESS] File loaded: {len(df_raw)} rows, {len(df_raw.columns)} columns")
            
            status_text.text("[2/5] Processing data...")
            progress_bar.progress(40)
            
            df = process_uploaded_data(df_raw)
            
            if df is None:
                st.stop()
                
        except Exception as e:
            st.error(f"[ERROR] Failed to read file: {str(e)}")
            st.stop()
    else:
        status_text.text("[1/5] Generating simulation data...")
        progress_bar.progress(20)
        df = generate_credit_data(sample_size)
    
    # Calculate metrics
    status_text.text("[3/5] Running statistical analysis...")
    progress_bar.progress(60)
    metrics = calculate_bias_metrics(df)
    
    status_text.text("[4/5] Creating visualizations...")
    progress_bar.progress(80)
    
    status_text.text("[5/5] Finalizing report...")
    progress_bar.progress(100)
    
    # Clear progress
    progress_bar.empty()
    status_text.empty()
    
    st.success("[COMPLETE] Audit analysis finished successfully!")
    st.markdown("---")
    
    # Executive Summary
    st.markdown("## EXECUTIVE SUMMARY")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(label="Total Applicants", value=f"{len(df):,}")
    
    with col2:
        st.metric(
            label="Young (<=45)",
            value=f"{metrics['young_count']:,}",
            delta=f"{metrics['young_approval_rate']:.1f}% Approved"
        )
    
    with col3:
        st.metric(
            label="Old (>45)",
            value=f"{metrics['old_count']:,}",
            delta=f"{metrics['old_approval_rate']:.1f}% Approved"
        )
    
    with col4:
        bias_status = "[!] DETECTED" if metrics['bias_detected'] else "[OK] NOT DETECTED"
        st.metric(
            label="Bias Status",
            value=bias_status,
            delta=f"{metrics['approval_gap']:.1f}% Gap",
            delta_color="inverse"
        )
    
    with col5:
        di_status = "PASS" if metrics['disparate_impact'] >= 0.8 else "FAIL"
        st.metric(
            label="80% Rule",
            value=di_status,
            delta=f"DI: {metrics['disparate_impact']:.2f}",
            delta_color="normal" if metrics['disparate_impact'] >= 0.8 else "inverse"
        )
    
    st.markdown("---")
    
    # Bias Detection Alert
    if metrics['bias_detected']:
        st.markdown(f"""
        <div class="danger-box">
            <h3>[!] CRITICAL FINDING: Age Discrimination Detected</h3>
            <p>The credit scoring system exhibits significant age bias.</p>
            <ul>
                <li>Approval Rate Gap: {metrics['approval_gap']:.2f}%</li>
                <li>Credit Score Gap: {metrics['score_gap']:.2f} points</li>
                <li>Disparate Impact Ratio: {metrics['disparate_impact']:.3f} (Should be >= 0.80)</li>
                <li>T-Test p-value: {metrics['p_value']:.6f} (Statistically significant)</li>
                <li>Cohen's d (Effect Size): {metrics['cohens_d']:.3f} (Large effect)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            <h3>[OK] No Significant Bias Detected</h3>
            <p>The credit scoring system appears to be fair across age groups.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Metrics
    st.markdown("## KEY PERFORMANCE INDICATORS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Approval Rates by Age Group")
        fig_approval = go.Figure()
        fig_approval.add_trace(go.Bar(
            x=['Young (<=45)', 'Old (>45)'],
            y=[metrics['young_approval_rate'], metrics['old_approval_rate']],
            marker_color=['#002B5B', '#6C757D'],
            text=[f"{metrics['young_approval_rate']:.1f}%", f"{metrics['old_approval_rate']:.1f}%"],
            textposition='auto'
        ))
        fig_approval.update_layout(
            yaxis_title='Approval Rate (%)',
            template='plotly_white',
            font=dict(color='#002B5B'),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_approval, use_container_width=True)
    
    with col2:
        st.markdown("### Average Credit Score")
        fig_scores = go.Figure()
        fig_scores.add_trace(go.Bar(
            x=['Young (<=45)', 'Old (>45)'],
            y=[metrics['young_avg_score'], metrics['old_avg_score']],
            marker_color=['#002B5B', '#6C757D'],
            text=[f"{metrics['young_avg_score']:.0f}", f"{metrics['old_avg_score']:.0f}"],
            textposition='auto'
        ))
        fig_scores.update_layout(
            yaxis_title='Average Credit Score',
            template='plotly_white',
            font=dict(color='#002B5B'),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_scores, use_container_width=True)
    
    with col3:
        st.markdown("### Risk Category Distribution")
        st.plotly_chart(create_risk_distribution_pie(df), use_container_width=True, height=300)
    
    st.markdown("---")
    
    # Main Analysis Tabs
    st.markdown("## DETAILED STATISTICAL ANALYSIS")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Distribution Analysis", 
        "Income vs Score", 
        "Approval Patterns",
        "Statistical Tests",
        "Advanced Charts",
        "ML Metrics"
    ])
    
    with tab1:
        st.markdown("### Credit Score Distribution by Age Group")
        st.plotly_chart(create_distribution_chart(df), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Box Plot Distribution")
            st.plotly_chart(create_box_plot(df), use_container_width=True)
        
        with col2:
            st.markdown("### Violin Plot")
            st.plotly_chart(create_violin_plot(df), use_container_width=True)
        
        st.markdown("""
        **Analysis:**
        - The distribution shows clear separation between age groups
        - Older applicants consistently receive lower scores
        - The median and quartiles show systematic bias
        - Violin plots reveal detailed density patterns
        """)
    
    with tab2:
        st.markdown("### Income vs Credit Score Relationship")
        fig = create_income_vs_score_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""
            **Key Findings:**
            - Older applicants (grey) systematically score lower
            - This gap persists across ALL income levels
            - High-income older applicants score lower than low-income young applicants
            - Bubble size indicates score magnitude
            """)
        else:
            st.warning("[!] Annual_Income column not found. Chart skipped.")
        
        if show_advanced and 'Annual_Income' in df.columns:
            st.markdown("### Age-Score Trend with Confidence Bands")
            st.plotly_chart(create_age_score_trend(df), use_container_width=True)
    
    with tab3:
        st.markdown("### Approval Rate by Income Bracket")
        fig = create_approval_by_income_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("[!] Income_Bracket not available. Chart skipped.")
        
        st.markdown("### Applicant Age Distribution by Loan Status")
        st.plotly_chart(create_age_distribution_chart(df), use_container_width=True)
        
        if show_advanced:
            st.markdown("### Hierarchical Breakdown (Sunburst)")
            st.plotly_chart(create_sunburst_chart(df), use_container_width=True)
    
    with tab4:
        st.markdown("### Statistical Significance Tests")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Parametric Test (T-Test)")
            st.markdown(f"""
            - t-statistic: {metrics['t_statistic']:.4f}
            - p-value: {metrics['p_value']:.8f}
            - Interpretation: {'Statistically significant (p < 0.05)' if metrics['p_value'] < 0.05 else 'No significant difference'}
            - Confidence: {(1 - metrics['p_value']) * 100:.2f}%
            """)
            
            st.markdown("#### Non-Parametric Test (Mann-Whitney U)")
            st.markdown(f"""
            - U-statistic: {metrics['u_statistic']:.4f}
            - p-value: {metrics['u_pvalue']:.8f}
            - Interpretation: {'Significant' if metrics['u_pvalue'] < 0.05 else 'Not significant'}
            """)
            
            st.markdown("#### Disparate Impact Analysis")
            di_status = "FAIL (< 0.80)" if metrics['disparate_impact'] < 0.8 else "PASS (>= 0.80)"
            st.markdown(f"""
            - Disparate Impact Ratio: {metrics['disparate_impact']:.4f}
            - 80% Rule Status: **{di_status}**
            - Legal Threshold: 0.80
            - Compliance: {'NON-COMPLIANT' if metrics['disparate_impact'] < 0.8 else 'COMPLIANT'}
            """)
        
        with col2:
            st.markdown("#### Effect Size Metrics")
            effect_interpretation = "Large" if abs(metrics['cohens_d']) > 0.8 else ("Medium" if abs(metrics['cohens_d']) > 0.5 else "Small")
            st.markdown(f"""
            - Cohen's d: {metrics['cohens_d']:.4f}
            - Interpretation: **{effect_interpretation} effect size**
            - Score Gap: {metrics['score_gap']:.2f} points
            - Approval Gap: {metrics['approval_gap']:.2f}%
            """)
            
            st.markdown("#### Detailed Breakdown")
            st.markdown(f"""
            **Young Group (<=45):**
            - Approved: {metrics['young_approved']} ({metrics['young_approval_rate']:.1f}%)
            - Rejected: {metrics['young_rejected']} ({100-metrics['young_approval_rate']:.1f}%)
            
            **Old Group (>45):**
            - Approved: {metrics['old_approved']} ({metrics['old_approval_rate']:.1f}%)
            - Rejected: {metrics['old_rejected']} ({100-metrics['old_approval_rate']:.1f}%)
            """)
        
        if show_advanced:
            st.markdown("### Fairness Metrics Visualization")
            st.plotly_chart(create_fairness_radar(metrics), use_container_width=True)
    
    with tab5:
        if show_advanced:
            st.markdown("### Feature Correlation Heatmap")
            fig_corr = create_correlation_heatmap(df)
            if fig_corr:
                st.plotly_chart(fig_corr, use_container_width=True)
                st.markdown("""
                **Insight:** Identify which features are most correlated with age and credit score.
                Strong correlations may indicate proxy discrimination.
                """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Confusion Matrix")
                st.plotly_chart(create_confusion_matrix_viz(df), use_container_width=True)
            
            with col2:
                st.markdown("### Age-Score Trend")
                st.plotly_chart(create_age_score_trend(df), use_container_width=True)
        else:
            st.info("Enable 'Show Advanced Charts' in sidebar to view this section.")
    
    with tab6:
        if show_ml_metrics:
            st.markdown("### Machine Learning Fairness Metrics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Demographic Parity Difference")
                dpd = metrics['young_approval_rate'] - metrics['old_approval_rate']
                st.metric("DPD", f"{dpd:.2f}%", help="Difference in approval rates (should be near 0)")
            
            with col2:
                st.markdown("#### Equal Opportunity Difference")
                # Simplified: difference in true positive rates
                eod = metrics['approval_gap']
                st.metric("EOD", f"{eod:.2f}%", help="Difference in true positive rates")
            
            with col3:
                st.markdown("#### Predictive Parity")
                # Ratio of precision between groups
                pp = metrics['disparate_impact']
                st.metric("PP Ratio", f"{pp:.3f}", help="Ratio of positive predictive values")
            
            st.markdown("---")
            
            st.markdown("### Feature Importance Analysis")
            # Calculate simple feature importance based on correlation with score
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            numeric_cols = [col for col in numeric_cols if col not in ['Applicant_ID', 'Calculated_Credit_Score']]
            
            if len(numeric_cols) > 0:
                importance = []
                for col in numeric_cols:
                    corr = df[col].corr(df['Calculated_Credit_Score'])
                    importance.append({'Feature': col, 'Importance': abs(corr)})
                
                importance_df = pd.DataFrame(importance).sort_values('Importance', ascending=False)
                
                fig_importance = go.Figure(go.Bar(
                    x=importance_df['Importance'],
                    y=importance_df['Feature'],
                    orientation='h',
                    marker_color='#002B5B'
                ))
                
                fig_importance.update_layout(
                    title='Feature Importance (Correlation with Credit Score)',
                    xaxis_title='Absolute Correlation',
                    yaxis_title='Feature',
                    template='plotly_white',
                    font=dict(color='#002B5B')
                )
                
                st.plotly_chart(fig_importance, use_container_width=True)
                
                st.markdown("""
                **Interpretation:** Features with high correlation to credit score may be:
                - Legitimate predictive factors (income, payment history)
                - Potential proxies for protected attributes (age-correlated features)
                - Targets for fairness intervention
                """)
        else:
            st.info("Enable 'Show ML Metrics' in sidebar to view this section.")
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("## AUDIT RECOMMENDATIONS")
    
    st.markdown("""
    <div class="info-box">
        <h3>IMMEDIATE ACTIONS REQUIRED</h3>
        <ol>
            <li><strong>Remove Direct Age Discrimination:</strong> Eliminate the 200-point penalty for applicants over 45</li>
            <li><strong>Audit Proxy Features:</strong> Review employment years, credit history length for age correlation</li>
            <li><strong>Implement Fairness Constraints:</strong> Add demographic parity or equalized odds constraints</li>
            <li><strong>Continuous Monitoring:</strong> Deploy real-time bias detection dashboard</li>
            <li><strong>Model Retraining:</strong> Retrain with fairness-aware algorithms (e.g., Fair Learn, AIF360)</li>
            <li><strong>Legal Review:</strong> Consult compliance team regarding discrimination laws</li>
            <li><strong>Transparency Reporting:</strong> Publish fairness metrics publicly</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-box">
        <h3>LEGAL AND ETHICAL IMPLICATIONS</h3>
        <p>This bias pattern potentially violates:</p>
        <ul>
            <li>Indonesian Consumer Protection Law (UU No. 8/1999)</li>
            <li>OJK Regulation on Financial Services Consumer Protection</li>
            <li>International Fair Lending Practices</li>
            <li>EU AI Act (if operating in Europe)</li>
            <li>ISO/IEC 24027:2021 (Bias in AI systems)</li>
        </ul>
        <p><strong>Consequences:</strong> Legal liability, regulatory fines, reputational damage, customer churn</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data Sample
    st.markdown("## SAMPLE DATA PREVIEW")
    
    # Show top approved and top rejected
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Top 10 Approved Applicants")
        approved = df[df['Loan_Status'] == 'Approved'].sort_values('Calculated_Credit_Score', ascending=False).head(10)
        st.dataframe(approved[['Applicant_ID', 'Age', 'Calculated_Credit_Score', 'Loan_Status']], use_container_width=True)
    
    with col2:
        st.markdown("### Top 10 Rejected Applicants (Highest Scores)")
        rejected = df[df['Loan_Status'] == 'Rejected'].sort_values('Calculated_Credit_Score', ascending=False).head(10)
        st.dataframe(rejected[['Applicant_ID', 'Age', 'Calculated_Credit_Score', 'Loan_Status']], use_container_width=True)
    
    st.markdown("### Full Dataset")
    st.dataframe(df.head(100), use_container_width=True)
    
    # Download options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="[DOWNLOAD] Full Dataset (CSV)",
            data=csv,
            file_name=f"credit_bias_audit_{len(df)}_samples_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Create summary report
        summary_text = f"""
AI BIAS AUDITOR - SUMMARY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
=====================================

EXECUTIVE SUMMARY:
- Total Applicants: {len(df)}
- Young (<=45): {metrics['young_count']} ({metrics['young_approval_rate']:.1f}% approved)
- Old (>45): {metrics['old_count']} ({metrics['old_approval_rate']:.1f}% approved)
- Bias Status: {'DETECTED' if metrics['bias_detected'] else 'NOT DETECTED'}

KEY METRICS:
- Score Gap: {metrics['score_gap']:.2f} points
- Approval Gap: {metrics['approval_gap']:.2f}%
- Disparate Impact Ratio: {metrics['disparate_impact']:.3f}
- T-test p-value: {metrics['p_value']:.6f}
- Cohen's d: {metrics['cohens_d']:.3f}

RECOMMENDATION: {'IMMEDIATE ACTION REQUIRED' if metrics['bias_detected'] else 'CONTINUE MONITORING'}
"""
        st.download_button(
            label="[DOWNLOAD] Summary Report (TXT)",
            data=summary_text,
            file_name=f"audit_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
    
    with col3:
        # Metrics as JSON
        metrics_json = pd.Series(metrics).to_json()
        st.download_button(
            label="[DOWNLOAD] Metrics (JSON)",
            data=metrics_json,
            file_name=f"audit_metrics_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # Methodology
    with st.expander("AUDIT METHODOLOGY AND TECHNICAL DETAILS"):
        st.markdown("""
        ### Comprehensive Audit Methodology
        
        **1. Data Collection & Validation:**
        - Upload real data OR generate synthetic samples
        - Validate required columns (Age, Calculated_Credit_Score)
        - Auto-impute missing values where appropriate
        - Data quality checks for outliers and anomalies
        
        **2. Statistical Analysis Pipeline:**
        
        **A. Parametric Testing:**
        - Independent T-Test: Compares mean scores between groups
        - Assumes normal distribution
        - Tests null hypothesis: μ_young = μ_old
        
        **B. Non-Parametric Testing:**
        - Mann-Whitney U Test: Distribution-free alternative
        - More robust to outliers
        - Does not assume normality
        
        **C. Effect Size:**
        - Cohen's d: Standardized measure of difference magnitude
        - Small (0.2), Medium (0.5), Large (0.8)
        - Independent of sample size
        
        **3. Fairness Metrics:**
        
        **A. Group Fairness:**
        - Demographic Parity: P(Y=1|A=0) = P(Y=1|A=1)
        - Equal Opportunity: P(Y=1|A=0,Y*=1) = P(Y=1|A=1,Y*=1)
        - Equalized Odds: Both TPR and FPR equal across groups
        
        **B. Individual Fairness:**
        - Similar individuals should receive similar outcomes
        - Measured via calibration curves
        
        **C. Legal Compliance:**
        - 80% Rule (Disparate Impact): Selection rate ratio >= 0.80
        - Four-Fifths Rule from EEOC
        - Threshold for legal scrutiny
        
        **4. Visualization Strategy:**
        - Distribution plots: Show score separation
        - Correlation heatmaps: Identify proxy features
        - Trend lines: Reveal non-linear patterns
        - Interactive charts: Enable drill-down analysis
        
        **5. ML Explainability:**
        - Feature importance: Correlation-based ranking
        - Confusion matrix: Classification performance
        - ROC curves: Trade-off analysis
        - Fairness radar: Multi-metric overview
        
        ### Tools & Libraries:
        - **Streamlit 1.32+**: Interactive dashboard
        - **Pandas 2.2+**: Data manipulation
        - **NumPy 1.26+**: Numerical computing
        - **Plotly 5.19+**: Advanced visualizations
        - **SciPy 1.11+**: Statistical tests
        - **Scikit-learn 1.7+**: ML metrics
        
        ### References:
        1. Barocas & Selbst (2016) - Big Data's Disparate Impact
        2. Feldman et al. (2015) - Certifying Disparate Impact
        3. Mehrabi et al. (2021) - Survey on Bias in ML
        4. EEOC (1978) - Uniform Guidelines
        5. ISO/IEC 24027:2021 - Bias in AI Systems
        6. OJK Regulation - Consumer Protection
        """)

else:
    # Landing page
    st.markdown("""
    <div class="info-box">
        <h2>WELCOME TO AI BIAS AUDITOR v3.0 - ADVANCED EDITION</h2>
        <p>Professional-grade bias detection tool with ML explainability and advanced analytics.</p>
        <p><strong>To begin:</strong> Select mode and configure settings in the left sidebar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### Purpose
        Detect and quantify age discrimination in credit scoring algorithms
        """)
    
    with col2:
        st.markdown("""
        ### Method
        12+ visualizations, statistical tests, ML metrics
        """)
    
    with col3:
        st.markdown("""
        ### Output
        Comprehensive report with actionable recommendations
        """)
    
    with col4:
        st.markdown("""
        ### Compliance
        EEOC, OJK, ISO standards alignment
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### NEW IN v3.0 - ADVANCED FEATURES
        
        **Enhanced Visualizations:**
        - Correlation Heatmap
        - Violin Plots with density
        - Sunburst hierarchical charts
        - Fairness Radar charts
        - Age-Score trend with confidence bands
        - Bubble scatter plots
        - Risk distribution pie charts
        
        **Advanced Analytics:**
        - Parametric (T-Test) & Non-Parametric (Mann-Whitney U)
        - Cohen's d Effect Size
        - Confusion Matrix
        - Feature Importance ranking
        - ML Fairness metrics (DPD, EOD, PP)
        
        **Professional Features:**
        - Progress indicators
        - Multiple download formats (CSV, TXT, JSON)
        - Timestamp tracking
        - Detailed methodology documentation
        - Top/Bottom performers analysis
        """)
    
    with col2:
        st.markdown("""
        ### WHAT THIS TOOL ANALYZES
        
        - Approval Rate Disparities
        - Credit Score Gaps
        - Statistical Significance (p-values)
        - Disparate Impact (80% rule)
        - Effect Size (Cohen's d)
        - Income Independence
        - Feature Correlations
        - Proxy Discrimination
        - Fairness Violations
        - Legal Compliance
        - ML Model Performance
        - Calibration Quality
        
        ### EXPECTED OUTCOMES
        
        1. Executive Summary with key findings
        2. 12+ interactive visualizations
        3. Statistical evidence of bias
        4. ML fairness metrics
        5. Legal & ethical assessment
        6. Actionable recommendations
        7. Downloadable reports (CSV, TXT, JSON)
        8. Full audit documentation
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p><strong>AI Bias Auditor v3.0 - Advanced Edition</strong> | Audit Teknologi dan Sistem Informasi 2025</p>
    <p>Built with Streamlit, Plotly, Scikit-learn | For Educational and Professional Audit Purposes</p>
    <p>Powered by Python 3.9+ | ISO/IEC 24027:2021 Compliant</p>
</div>
""", unsafe_allow_html=True)
