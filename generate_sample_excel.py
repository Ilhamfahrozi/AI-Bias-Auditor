"""
Script to generate sample Excel file for AI Bias Auditor
This creates realistic credit scoring data with embedded age bias
"""

import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(123)

# Generate 100 sample applicants
n = 100

data = {
    'Applicant_ID': [f'APP{str(i).zfill(5)}' for i in range(1, n + 1)],
    'Age': np.random.randint(20, 65, n),
    'Annual_Income': np.random.randint(50000000, 400000000, n),
    'Employment_Years': np.random.randint(1, 35, n),
    'Debt_to_Income_Ratio': np.random.uniform(0.1, 0.5, n).round(2),
    'Credit_History_Length': np.random.randint(1, 25, n)
}

df = pd.DataFrame(data)

# Calculate base credit score
income_normalized = (df['Annual_Income'] - df['Annual_Income'].min()) / (df['Annual_Income'].max() - df['Annual_Income'].min())
base_score = 400 + (income_normalized * 350)
base_score += df['Employment_Years'] * 2
base_score -= df['Debt_to_Income_Ratio'] * 80
base_score += df['Credit_History_Length'] * 3

# Add random variation
base_score += np.random.randint(-40, 40, n)

df['Calculated_Credit_Score'] = base_score

# SIMULATE BIAS: Penalize applicants over 45
df.loc[df['Age'] > 45, 'Calculated_Credit_Score'] -= 180

# Clip to valid range
df['Calculated_Credit_Score'] = df['Calculated_Credit_Score'].clip(300, 850).astype(int)

# Determine loan status
df['Loan_Status'] = df['Calculated_Credit_Score'].apply(
    lambda x: 'Approved' if x >= 600 else 'Rejected'
)

# Format income for readability
df['Annual_Income_Formatted'] = df['Annual_Income'].apply(lambda x: f'Rp {x:,}')

# Save to Excel with multiple sheets
with pd.ExcelWriter('sample_credit_data_complete.xlsx', engine='openpyxl') as writer:
    # Sheet 1: Full data
    df.to_excel(writer, sheet_name='Full Data', index=False)
    
    # Sheet 2: Minimal (hanya required columns)
    df[['Applicant_ID', 'Age', 'Calculated_Credit_Score']].to_excel(
        writer, sheet_name='Minimal Data', index=False
    )
    
    # Sheet 3: With income (for better analysis)
    df[['Applicant_ID', 'Age', 'Annual_Income', 'Calculated_Credit_Score', 'Loan_Status']].to_excel(
        writer, sheet_name='With Income', index=False
    )
    
    # Sheet 4: Summary statistics
    summary = pd.DataFrame({
        'Metric': [
            'Total Applicants',
            'Young (<=45)',
            'Old (>45)',
            'Avg Score (Young)',
            'Avg Score (Old)',
            'Approval Rate (Young)',
            'Approval Rate (Old)'
        ],
        'Value': [
            len(df),
            len(df[df['Age'] <= 45]),
            len(df[df['Age'] > 45]),
            df[df['Age'] <= 45]['Calculated_Credit_Score'].mean().round(2),
            df[df['Age'] > 45]['Calculated_Credit_Score'].mean().round(2),
            f"{(df[df['Age'] <= 45]['Loan_Status'] == 'Approved').sum() / len(df[df['Age'] <= 45]) * 100:.1f}%",
            f"{(df[df['Age'] > 45]['Loan_Status'] == 'Approved').sum() / len(df[df['Age'] > 45]) * 100:.1f}%"
        ]
    })
    summary.to_excel(writer, sheet_name='Summary', index=False)

print("✓ File Excel berhasil dibuat: sample_credit_data_complete.xlsx")
print(f"✓ Total data: {len(df)} applicants")
print(f"✓ Sheets: Full Data, Minimal Data, With Income, Summary")
print("\nPreview data:")
print(df.head(10))
print("\nStatistik:")
print(f"- Young (<=45): {len(df[df['Age'] <= 45])} applicants")
print(f"- Old (>45): {len(df[df['Age'] > 45])} applicants")
print(f"- Avg score (Young): {df[df['Age'] <= 45]['Calculated_Credit_Score'].mean():.1f}")
print(f"- Avg score (Old): {df[df['Age'] > 45]['Calculated_Credit_Score'].mean():.1f}")
