import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
from statsmodels.tsa.arima_model import ARIMA
from itertools import combinations
from scipy import stats

# Load the CSV files into DataFrames
purchase_data = pd.read_csv("C:\\Users\\user\\Documents\\quantium\\QVI_purchase_behaviour.csv")
transaction_data = pd.read_csv("C:\\Users\\user\\Documents\\quantium\\QVI_transaction_data.csv")
# Merge the tables based on 'Customer_ID'
merged_data = pd.merge(purchase_data, transaction_data, on='Customer_ID')

# Group by lifestage
grouped_data = merged_data.groupby('Lifestage')
# Calculate various statistics
results = grouped_data.agg({
    'Transaction_ID': 'count',
    'Customer_ID': 'nunique',
    'Category': lambda x: x.value_counts().idxmax(),
    'Product_name': lambda x: x.value_counts().idxmax(),
    'Product_Quality': 'mean',
    'Total_Sales': ['sum', 'mean']
})
# Rename the columns for clarity
results.columns = ['Total_Transactions', 'Total_Customers', 'Most_Popular_Category',
                   'Most_Popular_Product', 'Average_Quality', 'Total_Sales', 'Average_Sales']
results.to_csv("lifestage_analysis_results.csv")

# Group by Category
grouped_data = merged_data.groupby('Category')
# Calculate various statistics
results = grouped_data.agg({
    'Transaction_ID': 'count',
    'Customer_ID': 'nunique',
    'Product_name': lambda x: x.value_counts().idxmax(),
    'Product_name': lambda x: x.value_counts().idxmin(),
    'Product_Quality': 'mean',
    'Total_Sales': 'sum'
})
# Rename the columns for clarity
results.columns = ['Total_Transactions', 'Total_Customers', 'Most_Popular_Product',
                   'Least_Popular_Product', 'Average_Quality', 'Total_Sales', 'Average_Sales']
results.to_csv("category_analysis_results.csv")

#Store
grouped_data = merged_data.groupby('Store')
# Calculate various statistics
results = grouped_data.agg({
    'Transaction_ID': 'count',
    'Customer_ID': 'nunique',
    'Product_name': lambda x: x.value_counts().idxmax(),
    'Product_name': lambda x: x.value_counts().idxmin(),
    'Product_Quality': 'mean',
    'Total_Sales': 'sum',
    'Total_Sales': 'sum'
})
# Rename the columns for clarity
results.columns = ['Total_Transactions', 'Total_Customers', 'Most_Popular_Product',
                   'Least_Popular_Product', 'Average_Quality', 'Total_Sales', 'Average_Sales']
results.to_csv("store_analysis_results.csv")


#Date analysis
# Convert the 'DATE' column to a Pandas datetime object
merged_data['DATE'] = pd.to_datetime(merged_data['DATE'])
# Extract the month from the 'DATE' column and store it in a new column
merged_data['Month'] = merged_data['DATE'].dt.month
# Group the data by month and calculate the total sales per month
monthly_total_sales = merged_data.groupby('Month')['Total_Sales'].sum()
# Group the data by month and calculate the total unique customers per month
monthly_unique_customers = merged_data.groupby('Month')['Customer_ID'].nunique()
# Group the data by month and calculate the total transaction counts per month
monthly_transaction_counts = merged_data.groupby('Month')['Transaction_ID'].count()
# Group the data by month and calculate the average product quality per month
monthly_average_quality = merged_data.groupby('Month')['Product_Quality'].mean()
# Create a list of month names for labeling the x-axis
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# Plot the data
plt.figure(figsize=(12, 8))
# Total Sales per Month
plt.subplot(2, 2, 1)
monthly_total_sales.plot(kind='bar', color='skyblue')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.title('Total Sales per Month')
plt.xticks(range(12), month_names, rotation=0)
# Total Unique Customers per Month
plt.subplot(2, 2, 2)
monthly_unique_customers.plot(kind='bar', color='lightcoral')
plt.xlabel('Month')
plt.ylabel('Total Unique Customers')
plt.title('Total Unique Customers per Month')
plt.xticks(range(12), month_names, rotation=0)
# Total Transaction Counts per Month
plt.subplot(2, 2, 3)
monthly_transaction_counts.plot(kind='bar', color='lightgreen')
plt.xlabel('Month')
plt.ylabel('Total Transaction Counts')
plt.title('Total Transaction Counts per Month')
plt.xticks(range(12), month_names, rotation=0)
# Average Product Quality per Month
plt.subplot(2, 2, 4)
monthly_average_quality.plot(kind='bar', color='lightblue')
plt.xlabel('Month')
plt.ylabel('Average Product Quality')
plt.title('Average Product Quality per Month')
plt.xticks(range(12), month_names, rotation=0)
plt.tight_layout()
plt.show()


#General Information
average_sales = merged_data['Total_Sales'].mean()
print(f"Average Sales: {average_sales}")
# Calculate Median
median_sales = merged_data['Total_Sales'].median()
print(f"Median Sales: {median_sales}")
# Calculate Standard Deviation
std_sales = merged_data['Total_Sales'].std()
print(f"Standard Deviation of Sales: {std_sales}")
# Calculate Percentiles
percentile_25 = merged_data['Total_Sales'].quantile(0.25)
percentile_75 = merged_data['Total_Sales'].quantile(0.75)
print(f"25th Percentile: {percentile_25}\n75th Percentile: {percentile_75}")

# Calculate Correlation
correlation_sales_quality = merged_data['Total_Sales'].corr(merged_data['Product_Quality'])
print(f"Correlation between Sales and Product Quality: {correlation_sales_quality}")
# Calculate Correlation between Customer_ID and Transaction_ID
correlation_customer_transaction = merged_data['Customer_ID'].corr(merged_data['Transaction_ID'])
print(f"Correlation between Customer_ID and Transaction_ID: {correlation_customer_transaction}")
# Calculate Correlation between Transactions_ID and Total_Sales
correlation_transaction_sales = merged_data['Transaction_ID'].corr(merged_data['Total_Sales'])
print(f"Correlation between Transactions_ID and Total_Sales: {correlation_transaction_sales}")


#Clusters
features = merged_data[['Total_Sales', 'Product_Quality']]
# Specify the number of clusters (you can choose an appropriate number)
n_clusters = 3
# Create a K-Means model and fit it to the data
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
kmeans.fit(features)
# Add the cluster labels to your DataFrame
merged_data['Product Cluster'] = kmeans.labels_
# Define segmentation criteria and labels
bins = [0, 10, 20, float('inf')]
labels = ['Low Value', 'Medium Value', 'High Value']
# Create a new column 'Customer Segment' based on total sales
merged_data['Customer Segment'] = pd.cut(merged_data['Total_Sales'], bins=bins, labels=labels)

# Scatter plot for clustering results
plt.scatter(merged_data['Total_Sales'], merged_data['Product_Quality'], c=merged_data['Product Cluster'])
plt.xlabel('Total Sales')
plt.ylabel('Product Quality')
plt.title('Product Clustering')
plt.show()
sns.countplot(data=merged_data, x='Customer Segment')
plt.xlabel('Segment')
plt.ylabel('Count')
plt.title('Customer Segmentation')
plt.show()
customer_segment_stats = merged_data.groupby('Customer Segment')['Total_Sales'].mean()
print(customer_segment_stats)


# Define month names for labeling the x-axis
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Fit an ARIMA model to the time series data
model = ARIMA(monthly_total_sales, order=(1, 1, 1))
model_fit = model.fit(disp=0)

# Forecast future sales
forecast_steps = 12  # Number of time steps to forecast
forecast, stderr, conf_int = model_fit.forecast(steps=forecast_steps)

# Visualize the forecast
plt.figure(figsize=(12, 6))
plt.plot(monthly_total_sales.index, monthly_total_sales, label='Observed')
plt.plot(range(len(monthly_total_sales), len(monthly_total_sales) + forecast_steps), forecast, label='Forecast', color='red')
plt.fill_between(range(len(monthly_total_sales), len(monthly_total_sales) + forecast_steps), conf_int[:, 0], conf_int[:, 1], color='pink', alpha=0.3)
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.title('Monthly Total Sales Forecast')
plt.legend()
plt.xticks(range(len(monthly_total_sales), len(monthly_total_sales) + forecast_steps), [month_names[i % 12] for i in range(len(monthly_total_sales), len(monthly_total_sales) + forecast_steps)])
plt.show()

## Typical significance level
lifestage_groups = [
    'YOUNG SINGLES/COUPLES',
    'YOUNG FAMILIES',
    'OLDER SINGLES/COUPLES',
    'MIDAGE SINGLES/COUPLES',
    'NEW FAMILIES',
    'OLDER FAMILIES',
    'RETIREES'
]
# Set the significance level (alpha)
alpha = 0.05  
# Create combinations of lifestage groups for comparison
combinations_list = list(combinations(lifestage_groups, 2))
for group1, group2 in combinations_list:
    group1_sales = merged_data[merged_data['Lifestage'] == group1]['Total_Sales']
    group2_sales = merged_data[merged_data['Lifestage'] == group2]['Total_Sales']
    # Perform a two-sample t-test for each pair of groups
    t_statistic, p_value = stats.ttest_ind(group1_sales, group2_sales)
    if p_value < alpha:
        print(f"Reject the null hypothesis: There is a significant difference in sales between {group1} and {group2}.")
    else:
        print(f"Fail to reject the null hypothesis: There is no significant difference in sales between {group1} and {group2}.")
resultslifestage_df = pd.DataFrame(results, columns=['Group1', 'Group2', 'T-Statistic', 'P-Value', 'Result'])


