"""
FUTURE_DS_01: Business Sales Performance Analytics
Module: Data Preprocessing & Cleaning Pipeline
Author: Future Interns - Data Science & Analytics Track
"""

import os
import pandas as pd
import numpy as np


def clean_sales_data(raw_data_path: str, output_cleaned_path: str = None) -> pd.DataFrame:
    """
    Ingests raw sales dataset, handles missing values and data inconsistencies,
    derives financial and temporal dimensions, and saves the cleaned dataset.
    """
    print(f"[*] Ingesting raw data from: {raw_data_path}")
    df = pd.read_csv(raw_data_path)

    # 1. Standardize date formats
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce')

    # Drop rows with null essential dates or order IDs
    df = df.dropna(subset=['Order_ID', 'Order_Date', 'Ship_Date']).copy()

    # 2. Text standardization & cleaning
    text_cols = ['Ship_Mode', 'Customer_Segment', 'Region', 'State', 'Category', 'Sub_Category', 'Product_Name']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # 3. Numeric sanitization and defaults
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(1).astype(int)
    df['Unit_Price'] = pd.to_numeric(df['Unit_Price'], errors='coerce').fillna(0.0).round(2)
    df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0.0).round(2)

    # Filter out invalid entries
    df = df[df['Quantity'] > 0].copy()
    df = df[df['Unit_Price'] >= 0].copy()

    # 4. Financial feature engineering
    # Gross Sales
    df['Gross_Sales'] = (df['Unit_Price'] * df['Quantity']).round(2)
    # Discount Amount
    df['Discount_Amount'] = (df['Gross_Sales'] * df['Discount']).round(2)
    # Net Sales (Actual revenue realized)
    df['Net_Sales'] = (df['Gross_Sales'] - df['Discount_Amount']).round(2)

    # Cost estimation if not present or inconsistent (assuming cost based on standard category margins)
    if 'Total_Cost' not in df.columns or df['Total_Cost'].isnull().any():
        cost_multiplier = {
            'Technology': 0.60,
            'Furniture': 0.75,
            'Office Supplies': 0.55
        }
        df['Total_Cost'] = df.apply(
            lambda r: round(r['Gross_Sales'] * cost_multiplier.get(r['Category'], 0.65), 2),
            axis=1
        )
    else:
        df['Total_Cost'] = pd.to_numeric(df['Total_Cost'], errors='coerce').fillna(df['Gross_Sales'] * 0.65).round(2)

    # Profit & Profit Margin
    df['Profit'] = (df['Net_Sales'] - df['Total_Cost']).round(2)
    df['Profit_Margin_Pct'] = np.where(
        df['Net_Sales'] > 0,
        ((df['Profit'] / df['Net_Sales']) * 100).round(2),
        0.0
    )
    df['Is_Profitable'] = df['Profit'] > 0

    # 5. Temporal feature engineering
    df['Shipping_Duration_Days'] = (df['Ship_Date'] - df['Order_Date']).dt.days
    df['Order_Year'] = df['Order_Date'].dt.year
    df['Order_Month'] = df['Order_Date'].dt.month
    df['Order_Month_Name'] = df['Order_Date'].dt.strftime('%b')
    df['Order_YearMonth'] = df['Order_Date'].dt.strftime('%Y-%m')
    df['Order_Quarter'] = 'Q' + df['Order_Date'].dt.quarter.astype(str)
    df['Day_of_Week'] = df['Order_Date'].dt.strftime('%A')

    # Sort chronological
    df = df.sort_values('Order_Date').reset_index(drop=True)

    if output_cleaned_path:
        os.makedirs(os.path.dirname(output_cleaned_path), exist_ok=True)
        df.to_csv(output_cleaned_path, index=False)
        print(f"[+] Cleaned data saved successfully to: {output_cleaned_path} ({len(df):,} records)")

    return df


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv = os.path.join(base_dir, 'data', 'raw_sales_data.csv')
    clean_csv = os.path.join(base_dir, 'data', 'cleaned_sales_data.csv')
    if os.path.exists(raw_csv):
        clean_sales_data(raw_csv, clean_csv)
    else:
        print(f"[!] Raw file not found at {raw_csv}")
