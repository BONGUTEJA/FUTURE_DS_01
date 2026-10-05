"""
FUTURE_DS_01: Business Sales Performance Analytics
Module: Publication-Ready Data Visualizations Generator
Author: Future Interns - Data Science & Analytics Track
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean professional styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8


def generate_all_figures(data_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

    # 1. Revenue & Profit Monthly Trend
    plt.figure(figsize=(14, 6))
    monthly = df.groupby('Order_YearMonth').agg({'Net_Sales': 'sum', 'Profit': 'sum'}).reset_index()
    x = range(len(monthly))
    plt.plot(x, monthly['Net_Sales'] / 1e3, marker='o', linewidth=2.5, color='#2563EB', label='Revenue ($k)')
    plt.plot(x, monthly['Profit'] / 1e3, marker='s', linewidth=2.5, color='#10B981', label='Profit ($k)')
    plt.fill_between(x, monthly['Profit'] / 1e3, monthly['Net_Sales'] / 1e3, color='#DBEAFE', alpha=0.5)
    plt.xticks(ticks=x, labels=monthly['Order_YearMonth'], rotation=45, ha='right', fontsize=9)
    plt.title('Monthly Revenue & Profit Performance (2023 - 2025)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Year - Month', fontsize=11, labelpad=10)
    plt.ylabel('Amount in Thousands ($ USD)', fontsize=11, labelpad=10)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_revenue_and_profit_monthly_trend.png'), dpi=300)
    plt.close()

    # 2. Top 10 Products by Revenue
    plt.figure(figsize=(12, 6))
    top_prod = df.groupby('Product_Name')['Net_Sales'].sum().reset_index()
    top_prod = top_prod.sort_values('Net_Sales', ascending=False).head(10)
    bars = plt.barh(top_prod['Product_Name'][::-1], top_prod['Net_Sales'][::-1] / 1e3, color='#3B82F6', edgecolor='#1D4ED8')
    plt.title('Top 10 Products by Net Revenue ($k)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Net Revenue in Thousands ($ USD)', fontsize=11, labelpad=10)
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 5, bar.get_y() + bar.get_height() / 2, f'${width:.1f}k', va='center', fontsize=9, fontweight='bold', color='#1E293B')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_top_10_products_revenue.png'), dpi=300)
    plt.close()

    # 3. Category & Sub-Category Profit Margins
    plt.figure(figsize=(12, 7))
    subcat = df.groupby(['Sub_Category', 'Category']).agg({'Net_Sales': 'sum', 'Profit': 'sum'}).reset_index()
    subcat['Margin'] = (subcat['Profit'] / subcat['Net_Sales']) * 100
    subcat = subcat.sort_values('Margin', ascending=True)
    colors = ['#EF4444' if m < 10 else '#10B981' for m in subcat['Margin']]
    plt.barh(subcat['Sub_Category'], subcat['Margin'], color=colors, edgecolor='#475569')
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(20, color='gray', linewidth=0.8, linestyle=':', label='Target Margin Threshold (20%)')
    plt.title('Profit Margin (%) by Sub-Category', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Profit Margin Percentage (%)', fontsize=11, labelpad=10)
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_category_subcat_profit_margins.png'), dpi=300)
    plt.close()

    # 4. Regional Performance Breakdown
    plt.figure(figsize=(10, 5))
    regional = df.groupby('Region').agg({'Net_Sales': 'sum', 'Profit': 'sum'}).reset_index()
    x = np.arange(len(regional))
    width = 0.35
    plt.bar(x - width/2, regional['Net_Sales'] / 1e3, width, label='Revenue ($k)', color='#3B82F6')
    plt.bar(x + width/2, regional['Profit'] / 1e3, width, label='Profit ($k)', color='#10B981')
    plt.xticks(x, regional['Region'], fontsize=11)
    plt.title('Regional Revenue vs Profit Performance', fontsize=14, fontweight='bold', pad=15)
    plt.ylabel('Amount in Thousands ($ USD)', fontsize=11)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_regional_performance_breakdown.png'), dpi=300)
    plt.close()

    # 5. Discount vs Profitability Scatter
    plt.figure(figsize=(10, 6))
    sample = df.sample(min(1000, len(df)), random_state=42)
    plt.scatter(sample['Discount'] * 100, sample['Profit_Margin_Pct'], alpha=0.6, c=sample['Profit_Margin_Pct'], cmap='coolwarm_r', edgecolors='none', s=40)
    plt.axhline(0, color='red', linestyle='--', linewidth=1, label='Break-even (0% Profit)')
    plt.title('Impact of Discount Rate on Profit Margin', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Discount Applied (%)', fontsize=11, labelpad=10)
    plt.ylabel('Profit Margin (%)', fontsize=11, labelpad=10)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_discount_vs_profitability_scatter.png'), dpi=300)
    plt.close()

    # 6. Customer Segment Analysis
    plt.figure(figsize=(10, 5))
    seg = df.groupby('Customer_Segment').agg({'Net_Sales': 'sum', 'Profit': 'sum', 'Order_ID': 'nunique'}).reset_index()
    plt.pie(seg['Net_Sales'], labels=seg['Customer_Segment'], autopct='%1.1f%%', startangle=140, colors=['#60A5FA', '#34D399', '#FBBF24'], wedgeprops=dict(width=0.4, edgecolor='white'))
    plt.title('Revenue Contribution by Customer Segment', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_customer_segment_analysis.png'), dpi=300)
    plt.close()

    print(f"[+] All 6 figures generated successfully in: {output_dir}")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_csv = os.path.join(base_dir, 'data', 'cleaned_sales_data.csv')
    fig_dir = os.path.join(base_dir, 'reports', 'figures')
    generate_all_figures(clean_csv, fig_dir)
