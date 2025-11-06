'''

'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

# Set up paths
in_dir = r'data/'
out_dir = r'outputs/'
os.makedirs(out_dir, exist_ok=True)
file_path = os.path.join(in_dir, 'SuperMarket_Analysis.csv')

# Load data
salesdf = pd.read_csv(file_path)
print(salesdf.head())
print(salesdf.columns)
print(salesdf.info())
print(salesdf.describe())
print(salesdf.isnull().sum())

# Data cleaning and type conversion
cols_to_numeric = ['Quantity', 'Unit price', 'Tax 5%', 'Sales', 'cogs', 'gross margin percentage', 'gross income', 'Rating']
for c in cols_to_numeric:
    if c in salesdf.columns:
        salesdf[c] = pd.to_numeric(salesdf[c], errors='coerce').fillna(0)
salesdf['Date']=pd.to_datetime(salesdf['Date'], errors='coerce')

salesdf.dropna(subset=['Sales'], inplace=True)

# Basic statistics
print(f'Total Records: {len(salesdf)}')
print(f'Average Rating: {salesdf["Rating"].mean():.2f}')
print(f'Total Sales: {salesdf["Sales"].sum():.2f} USD')
print(f'Total Quantity Sold: {salesdf["Quantity"].sum()} items')

# Sales by Product Line
product_sales = salesdf.groupby('Product line',dropna=False)['Sales'].sum().sort_values(ascending=False)
prod_df = product_sales.reset_index().rename(columns={'Sales':'TotalSales','Product line':'ProductLine'})   
print('Sales by Product Line:')
print(prod_df)

# Plot Sales by Product Line
fig1,ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data = prod_df,x='ProductLine', y='TotalSales', palette='viridis',ax=ax1)  
ax1.set_title('Total Sales by Product Line')
ax1.set_xlabel('Product Line')
ax1.set_ylabel('Total Sales (USD)')
ax1.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
for p in ax1.patches:
    height = p.get_height()
    ax1.annotate(f'{height:,.0f}',
                 (p.get_x() + p.get_width() / 2., height),
                 ha='center', va='bottom', fontsize=9, rotation=0, xytext=(0, 5),textcoords='offset points')
fig1.tight_layout()
fig1.savefig(os.path.join(out_dir,'sales_by_product_line.png'), bbox_inches='tight',dpi=150)
plt.close(fig1)
print(f'Chart saved to: {out_dir}sales_by_product_line.png')

# Sales by city
city_sales = salesdf.groupby('City')['Sales'].sum().sort_values(ascending=False)
city_df = city_sales.reset_index().rename(columns={'Sales':'TotalSales','City':'CityName'})
print('Sales by City:')
print(city_df)

# Plot Sales by City
fig2 , ax2 = plt.subplots(figsize=(max(8,len(city_df)*0.5), 6))
sns.barplot(data=city_df,x='CityName', y='TotalSales', palette='magma', ax=ax2)
ax2.set_title('Total Sales by City')
ax2.set_xlabel('City')
ax2.set_ylabel('Total Sales (USD)')
plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
for p in ax2.patches:
    height = p.get_height()
    ax2.annotate(f'{height:,.0f}',
                 (p.get_x() + p.get_width() / 2., height),
                 ha='center', va='bottom', fontsize=9, rotation=0, xytext=(0, 5),textcoords='offset points')
fig2.tight_layout()
fig2.savefig(os.path.join(out_dir,'sales_by_city.png'), bbox_inches='tight',dpi=150)
plt.close(fig2)
print(f'Chart saved to: {out_dir}sales_by_city.png')

# Sales by Gender
gender_sales=salesdf.groupby('Gender')['Sales'].sum().sort_values(ascending=False)
gender_df=gender_sales.reset_index().rename(columns={'Sales':'TotalSales','Gender':'Gender'})
print('Sales by Gender:')
print(gender_df)
# Plot Sales by Gender
fig3, ax3 = plt.subplots(figsize=(6, 6))
sns.barplot(data=gender_df,x='Gender', y='TotalSales', palette='Set2', ax=ax3)
ax3.set_title('Total Sales by Gender')
ax3.set_xlabel('Gender')
ax3.set_ylabel('Total Sales (USD)')
for p in ax3.patches:
    height = p.get_height()
    ax3.annotate(f'{height:,.0f}',
                 (p.get_x() + p.get_width() / 2., height),
                 ha='center', va='bottom', fontsize=9, rotation=0, xytext=(0, 5),textcoords='offset points')
fig3.tight_layout()
fig3.savefig(os.path.join(out_dir,'sales_by_gender.png'), bbox_inches='tight',dpi=150)
plt.close(fig3)
print(f'Chart saved to: {out_dir}sales_by_gender.png')
