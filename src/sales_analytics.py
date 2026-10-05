"""
FUTURE_DS_01: Business Sales Performance Analytics
Module: Sales Analytics Engine & KPI Calculations
Author: Future Interns - Data Science & Analytics Track
"""

import os
import json
import pandas as pd
import numpy as np


class SalesAnalyticsEngine:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)
        self.df['Order_Date'] = pd.to_datetime(self.df['Order_Date'])

    def compute_executive_kpis(self) -> dict:
        """Computes top-level executive KPIs."""
        total_rev = round(float(self.df['Net_Sales'].sum()), 2)
        total_prof = round(float(self.df['Profit'].sum()), 2)
        margin = round((total_prof / total_rev * 100), 2) if total_rev > 0 else 0.0
        total_orders = int(self.df['Order_ID'].nunique())
        unique_customers = int(self.df['Customer_ID'].nunique())
        aov = round(total_rev / total_orders, 2) if total_orders > 0 else 0.0

        return {
            "total_revenue": total_rev,
            "total_profit": total_prof,
            "profit_margin": margin,
            "total_orders": total_orders,
            "unique_customers": unique_customers,
            "aov": aov
        }

    def analyze_monthly_trends(self) -> pd.DataFrame:
        """Aggregates monthly revenue, profit, orders, and profit margin."""
        monthly = self.df.groupby('Order_YearMonth').agg(
            Revenue=('Net_Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Orders=('Order_ID', 'nunique'),
            Units_Sold=('Quantity', 'sum')
        ).reset_index()
        monthly['Revenue'] = monthly['Revenue'].round(2)
        monthly['Profit'] = monthly['Profit'].round(2)
        monthly['Profit_Margin_Pct'] = ((monthly['Profit'] / monthly['Revenue']) * 100).round(2)
        monthly['MoM_Revenue_Growth_Pct'] = monthly['Revenue'].pct_change().mul(100).round(2).fillna(0.0)
        return monthly

    def analyze_category_performance(self) -> pd.DataFrame:
        """Analyzes Category and Sub-Category revenue, profit, and margins."""
        cat_perf = self.df.groupby(['Category', 'Sub_Category']).agg(
            Revenue=('Net_Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Units_Sold=('Quantity', 'sum'),
            Avg_Discount=('Discount', 'mean')
        ).reset_index()
        cat_perf['Revenue'] = cat_perf['Revenue'].round(2)
        cat_perf['Profit'] = cat_perf['Profit'].round(2)
        cat_perf['Avg_Discount'] = (cat_perf['Avg_Discount'] * 100).round(2)
        cat_perf['Profit_Margin_Pct'] = ((cat_perf['Profit'] / cat_perf['Revenue']) * 100).round(2)
        return cat_perf.sort_values(by='Revenue', ascending=False)

    def analyze_product_performance(self, top_n: int = 10) -> pd.DataFrame:
        """Identifies top-selling products by Net Sales."""
        prod = self.df.groupby(['Product_Name', 'Category']).agg(
            Revenue=('Net_Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Units_Sold=('Quantity', 'sum')
        ).reset_index()
        prod['Revenue'] = prod['Revenue'].round(2)
        prod['Profit'] = prod['Profit'].round(2)
        prod['Profit_Margin_Pct'] = ((prod['Profit'] / prod['Revenue']) * 100).round(2)
        return prod.sort_values('Revenue', ascending=False).head(top_n)

    def analyze_regional_performance(self) -> pd.DataFrame:
        """Analyzes sales, profit, orders, and margin by geographic region."""
        region_df = self.df.groupby('Region').agg(
            Revenue=('Net_Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Orders=('Order_ID', 'nunique'),
            Customers=('Customer_ID', 'nunique')
        ).reset_index()
        region_df['Revenue'] = region_df['Revenue'].round(2)
        region_df['Profit'] = region_df['Profit'].round(2)
        region_df['Profit_Margin_Pct'] = ((region_df['Profit'] / region_df['Revenue']) * 100).round(2)
        return region_df.sort_values('Revenue', ascending=False)

    def analyze_customer_segments(self) -> pd.DataFrame:
        """Evaluates Consumer, Corporate, and Home Office segment metrics."""
        seg_df = self.df.groupby('Customer_Segment').agg(
            Revenue=('Net_Sales', 'sum'),
            Profit=('Profit', 'sum'),
            Orders=('Order_ID', 'nunique'),
            Unique_Customers=('Customer_ID', 'nunique')
        ).reset_index()
        seg_df['Revenue'] = seg_df['Revenue'].round(2)
        seg_df['Profit'] = seg_df['Profit'].round(2)
        seg_df['AOV'] = (seg_df['Revenue'] / seg_df['Orders']).round(2)
        seg_df['Revenue_Per_Customer'] = (seg_df['Revenue'] / seg_df['Unique_Customers']).round(2)
        seg_df['Profit_Margin_Pct'] = ((seg_df['Profit'] / seg_df['Revenue']) * 100).round(2)
        return seg_df.sort_values('Revenue', ascending=False)

    def export_full_metrics_json(self, output_path: str):
        """Exports key metrics to JSON format for web dashboards."""
        kpis = self.compute_executive_kpis()
        monthly = self.analyze_monthly_trends()
        regional = self.analyze_regional_performance()
        top_prod = self.analyze_product_performance(10)
        cat = self.df.groupby('Category')['Net_Sales'].sum().round(2)
        subcat = self.df.groupby('Sub_Category').apply(
            lambda g: round((g['Profit'].sum() / g['Net_Sales'].sum()) * 100, 2)
        ).sort_values()

        export_data = {
            **kpis,
            "monthly_labels": monthly['Order_YearMonth'].tolist(),
            "monthly_revenue": monthly['Revenue'].tolist(),
            "monthly_profit": monthly['Profit'].tolist(),
            "regions": regional['Region'].tolist(),
            "regional_revenue": regional['Revenue'].tolist(),
            "regional_profit": regional['Profit'].tolist(),
            "top_products": top_prod['Product_Name'].tolist(),
            "top_products_rev": top_prod['Revenue'].tolist(),
            "categories": cat.index.tolist(),
            "category_sales": cat.values.tolist(),
            "subcategories": subcat.index.tolist(),
            "subcat_margins": subcat.values.tolist()
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        print(f"[+] Metrics exported successfully to: {output_path}")


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_csv = os.path.join(base_dir, 'data', 'cleaned_sales_data.csv')
    metrics_json = os.path.join(base_dir, 'dashboards', 'sales_metrics.json')
    engine = SalesAnalyticsEngine(clean_csv)
    engine.export_full_metrics_json(metrics_json)
