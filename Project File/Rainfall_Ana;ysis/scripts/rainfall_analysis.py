"""
RAINFALL ANALYSIS FOR INDIAN AGRICULTURE
=========================================

A comprehensive data analysis project to understand rainfall patterns 
and support agricultural decision-making through data visualization, 
statistical analysis, and trend identification.

Author: Data Science Team
Date: 2026
Purpose: Support sustainable agriculture through data-driven insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Configure visualization styles
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11

def load_and_explore_data(filepath):
    """Load and explore the rainfall dataset."""
    print("=" * 80)
    print("📊 STEP 1: LOADING AND EXPLORING DATA")
    print("=" * 80)
    
    df = pd.read_csv(filepath)
    print(f"\n✅ Dataset loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:\n{df.head()}")
    print(f"\nData types:\n{df.dtypes}")
    
    return df

def clean_data(df):
    """Clean and preprocess the data."""
    print("\n" + "=" * 80)
    print("🧹 STEP 2: DATA CLEANING")
    print("=" * 80)
    
    # Remove duplicates
    df_clean = df.drop_duplicates().copy()
    print(f"Removed {len(df) - len(df_clean)} duplicate rows")
    
    # Handle negative values
    month_columns = [col for col in df.columns if col not in ['Year', 'State', 'Annual_Rainfall']]
    df_clean[month_columns] = df_clean[month_columns].clip(lower=0)
    print(f"Negative values forced to zero")
    
    # Verify data consistency
    print(f"\n✅ Data cleaning complete! Shape: {df_clean.shape}")
    return df_clean, month_columns

def analyze_monthly_rainfall(df, month_columns):
    """Analyze monthly rainfall patterns."""
    print("\n" + "=" * 80)
    print("📅 STEP 3: MONTHLY RAINFALL ANALYSIS")
    print("=" * 80)
    
    avg_monthly = df[month_columns].mean()
    peak_month = avg_monthly.idxmax()
    low_month = avg_monthly.idxmin()
    
    print(f"\nAverage Monthly Rainfall:")
    print(avg_monthly)
    print(f"\n⬆️ Peak: {peak_month} ({avg_monthly[peak_month]:.2f}mm)")
    print(f"⬇️ Lowest: {low_month} ({avg_monthly[low_month]:.2f}mm)")
    
    # Visualization
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(range(len(month_columns)), avg_monthly, color='steelblue', alpha=0.7)
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Rainfall (mm)')
    ax.set_title('Average Rainfall by Month')
    ax.set_xticks(range(len(month_columns)))
    ax.set_xticklabels(month_columns, rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/01_Monthly_Rainfall_Analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return avg_monthly, peak_month, low_month

def analyze_yearly_trends(df):
    """Analyze yearly rainfall trends."""
    print("\n" + "=" * 80)
    print("📈 STEP 4: YEARLY TREND ANALYSIS")
    print("=" * 80)
    
    yearly_rainfall = df.groupby('Year')['Annual_Rainfall'].mean()
    
    # Fit linear regression
    X = np.array(yearly_rainfall.index).reshape(-1, 1)
    y = np.array(yearly_rainfall.values)
    model = LinearRegression()
    model.fit(X, y)
    
    slope = model.coef_[0]
    trend = "INCREASING ⬆️" if slope > 0 else "DECREASING ⬇️"
    
    print(f"\nYearly Average Rainfall:")
    print(yearly_rainfall)
    print(f"\n📊 Trend: {trend} ({slope:.4f} mm/year)")
    
    # Visualization
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(yearly_rainfall.index, yearly_rainfall.values, marker='o', linewidth=2.5, label='Actual')
    ax.plot(yearly_rainfall.index, model.predict(X), '--', linewidth=2.5, label='Trend')
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Annual Rainfall (mm)')
    ax.set_title('Yearly Rainfall Trend')
    ax.legend()
    plt.tight_layout()
    plt.savefig('outputs/02_Yearly_Rainfall_Trend.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return yearly_rainfall

def analyze_state_rainfall(df):
    """Analyze rainfall by state."""
    print("\n" + "=" * 80)
    print("🗺️ STEP 5: STATE-WISE ANALYSIS")
    print("=" * 80)
    
    state_rainfall = df.groupby('State')['Annual_Rainfall'].agg(['mean', 'std']).sort_values('mean', ascending=False)
    
    print(f"\nRainfall by State:")
    print(state_rainfall)
    
    # Visualization
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.barh(state_rainfall.index, state_rainfall['mean'], color='steelblue', alpha=0.7)
    ax.set_xlabel('Average Annual Rainfall (mm)')
    ax.set_title('State-wise Rainfall Comparison')
    plt.tight_layout()
    plt.savefig('outputs/03_State_wise_Rainfall.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return state_rainfall

def analyze_seasonal_patterns(df, month_columns):
    """Analyze seasonal rainfall patterns."""
    print("\n" + "=" * 80)
    print("🌊 STEP 6: SEASONAL ANALYSIS")
    print("=" * 80)
    
    # Define seasons
    monsoon = ['June', 'July', 'August', 'September']
    winter = ['December', 'January', 'February']
    summer = ['March', 'April', 'May']
    
    monsoon_rain = df[monsoon].sum(axis=1).mean()
    winter_rain = df[winter].sum(axis=1).mean()
    summer_rain = df[summer].sum(axis=1).mean()
    
    seasons_data = {
        'Monsoon': monsoon_rain,
        'Winter': winter_rain,
        'Summer': summer_rain
    }
    
    print(f"\nSeasonal Average Rainfall:")
    for season, rainfall in seasons_data.items():
        print(f"  {season}: {rainfall:.2f}mm")
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(seasons_data.keys(), seasons_data.values(), color=['darkblue', 'lightblue', 'orange'], alpha=0.7)
    ax.set_ylabel('Average Rainfall (mm)')
    ax.set_title('Seasonal Rainfall Distribution')
    plt.tight_layout()
    plt.savefig('outputs/04_Seasonal_Analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return seasons_data

def predict_future_rainfall(df):
    """Predict future rainfall trends."""
    print("\n" + "=" * 80)
    print("🔮 STEP 7: RAINFALL PREDICTION")
    print("=" * 80)
    
    yearly_data = df.groupby('Year')['Annual_Rainfall'].mean()
    
    X = yearly_data.index.values.reshape(-1, 1)
    y = yearly_data.values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predictions
    future_years = np.array([2021, 2022, 2023, 2024, 2025]).reshape(-1, 1)
    predictions = model.predict(future_years)
    
    print(f"\nPredicted Annual Rainfall:")
    for year, pred in zip(future_years.flatten(), predictions):
        print(f"  {int(year)}: {pred:.2f}mm")
    
    # Evaluation
    r2 = r2_score(y, model.predict(X))
    print(f"\nModel R² Score: {r2:.4f}")
    
    return predictions

def generate_summary_report(df, avg_monthly, state_rainfall, seasons_data):
    """Generate executive summary."""
    print("\n" + "=" * 80)
    print("📋 EXECUTIVE SUMMARY")
    print("=" * 80)
    
    report = f"""
🌧️ RAINFALL ANALYSIS SUMMARY FOR INDIAN AGRICULTURE

KEY FINDINGS:
1. Average Annual Rainfall: {df['Annual_Rainfall'].mean():.0f}mm
2. Peak Rainfall Month: {avg_monthly.idxmax()} ({avg_monthly.max():.0f}mm)
3. Monsoon Contribution: {(seasons_data['Monsoon']/df['Annual_Rainfall'].mean()*100):.1f}%
4. Highest Rainfall State: {state_rainfall.index[0]}
5. Rainfall Variability: {df['Annual_Rainfall'].std():.0f}mm (std dev)

RECOMMENDATIONS:
✓ Focus on monsoon-dependent agriculture
✓ Develop irrigation for summer season
✓ Plan water storage for flood prevention
✓ Use seasonal forecasts for crop planning
✓ Implement drought management strategies
"""
    
    print(report)
    return report

def main():
    """Main analysis pipeline."""
    print("\n" + "🌧️ ".center(80) + "\n")
    print("RAINFALL ANALYSIS FOR INDIAN AGRICULTURE".center(80))
    print("=" * 80 + "\n")
    
    # Load data
    df = load_and_explore_data('data/rainfall_data.csv')
    
    # Clean data
    df_clean, month_columns = clean_data(df)
    
    # Analyses
    avg_monthly, peak_month, low_month = analyze_monthly_rainfall(df_clean, month_columns)
    yearly_rainfall = analyze_yearly_trends(df_clean)
    state_rainfall = analyze_state_rainfall(df_clean)
    seasons_data = analyze_seasonal_patterns(df_clean, month_columns)
    predictions = predict_future_rainfall(df_clean)
    
    # Summary
    report = generate_summary_report(df_clean, avg_monthly, state_rainfall, seasons_data)
    
    print("\n✅ ANALYSIS COMPLETE!")
    print("📊 All visualizations saved to 'outputs' folder")

if __name__ == "__main__":
    main()
