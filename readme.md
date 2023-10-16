# Quantium
Python

## Summary
Performed an analysis by grouping data based on lifestage, category, and store. Generated month-over-month charts to identify trends and conducted a descriptive analysis. Calculated correlations among key factors, segmented customers into Low, Medium, and High value groups, and visualized future sales forecasts. Additionally, assessed the significance of lifestage using an alpha point


## 1. Category of customers
![image](https://github.com/beishenov3197/quantium/assets/112967670/52d74d06-254c-46b3-b756-81df6d0c23ad)
- The majority of transactions were concentrated in the "Mainstream" and "Customers" categories, with the popular item being "RRD Steak" within this group.
- The "Premium" category demonstrated the highest average quality, and "Mainstream" stood out with the largest sales volume.
- In the "Budget" category, the product "Red Rock Deli Chikn&Garlic Aioli 150g" seems to offer a cost-effective option for customers while maintaining a decent product quality, resulting in substantial sales.

### 1. Code for category of customers
#### 1.1 Group by Category
grouped_data = merged_data.groupby('Category')
#### 1.2 Calculate various statistics
results = grouped_data.agg({
    'Transaction_ID': 'count',
    'Customer_ID': 'nunique',
    'Product_name': lambda x: x.value_counts().idxmax(),
    'Product_name': lambda x: x.value_counts().idxmin(),
    'Product_Quality': 'mean',
    'Total_Sales': 'sum'
})
#### 1.3 Renaming the columns for clarity
results.columns = ['Total_Transactions', 'Total_Customers', 'Most_Popular_Product',
                   'Least_Popular_Product', 'Average_Quality', 'Total_Sales', 'Average_Sales']

## 2. Analyzing of stores

![image](https://github.com/beishenov3197/quantium/assets/112967670/f4efdd02-a843-40ae-baae-9007a906cb00)

  - The dataset contains sales transaction information for various snack products in 242 different store transactions.
  - Product "Kettle Tortilla ChpsBtroot&Ricotta 150g" had the highest total sales of $12,802.45, followed by "Grain Waves Sweet Chilli 210g" with $14,647.65.
  - The average product quality for all items is around 1.73, indicating consistent product quality across the dataset.
  - Store 2 appears to be a high-performing store, with several top-selling products and total sales exceeding $17,000.
  - "Tostitos Smoked Chipotle 175g" had the highest product quality of approximately 2.01, suggesting a high level of customer satisfaction for this product.

### 2. Code for analyzing of stores
#Store
grouped_data = merged_data.groupby('Store')
#### Calculating various statistics
results = grouped_data.agg({
    'Transaction_ID': 'count',
    'Customer_ID': 'nunique',
    'Product_name': lambda x: x.value_counts().idxmax(),
    'Product_name': lambda x: x.value_counts().idxmin(),
    'Product_Quality': 'mean',
    'Total_Sales': 'sum',
    'Total_Sales': 'sum'
})
#### Renaming the columns for clarity
results.columns = ['Total_Transactions', 'Total_Customers', 'Most_Popular_Product',
                   'Least_Popular_Product', 'Average_Quality', 'Total_Sales', 'Average_Sales']

## 3. Lifestage analysis

![image](https://github.com/beishenov3197/quantium/assets/112967670/53840c5b-98cd-4989-93d2-aefe947b3c92)


- "Older Singles/Couples" and "Young Singles/Couples" have high transaction volumes and are important customer segments.
- "Budget" is the most popular category across lifestages, while "Thins Chips Light & Tangy 175g" is the top product for "Retirees."
- "Older Singles/Couples" lead in total sales and average sales per transaction, indicating their significance in generating revenue.

### 3. Code for lifestage analysis
#### Group by lifestage
grouped_data = merged_data.groupby('Lifestage')
#### Calculate various statistics
results = grouped_data.agg({
    'Transaction_ID': 'count',
    'Customer_ID': 'nunique',
    'Category': lambda x: x.value_counts().idxmax(),
    'Product_name': lambda x: x.value_counts().idxmax(),
    'Product_Quality': 'mean',
    'Total_Sales': ['sum', 'mean']
})
#### Rename the columns for clarity
results.columns = ['Total_Transactions', 'Total_Customers', 'Most_Popular_Category',
                   'Most_Popular_Product', 'Average_Quality', 'Total_Sales', 'Average_Sales']

## 4. Monthly Trends Analysis: Sales, Customers, Transactions, Quality
![Figure_1](https://github.com/beishenov3197/quantium/assets/112967670/a20091a6-25ce-44ba-a5ea-2a4d2677649f)
- Monthly trends exhibit stability with low volatility, indicating consistent performance throughout the year.
- February represents a month of lower performance, while December stands out with the highest performance across the observed metrics.
- These stable trends suggest effective management within the company, maintaining steady growth and minimizing drastic fluctuations.

### 4. Code for Monthly Trends Analysis
#### Convert the 'DATE' column to a Pandas datetime object
merged_data['DATE'] = pd.to_datetime(merged_data['DATE'])
#### Extract the month from the 'DATE' column and store it in a new column
merged_data['Month'] = merged_data['DATE'].dt.month
#### Group the data by month and calculate the total sales per month
monthly_total_sales = merged_data.groupby('Month')['Total_Sales'].sum()
#### Group the data by month and calculate the total unique customers per month
monthly_unique_customers = merged_data.groupby('Month')['Customer_ID'].nunique()
#### Group the data by month and calculate the total transaction counts per month
monthly_transaction_counts = merged_data.groupby('Month')['Transaction_ID'].count()
#### Group the data by month and calculate the average product quality per month
monthly_average_quality = merged_data.groupby('Month')['Product_Quality'].mean()
#### Create a list of month names for labeling the x-axis
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
### Plot the data
plt.figure(figsize=(12, 8))
#### Total Sales per Month
plt.subplot(2, 2, 1)
monthly_total_sales.plot(kind='bar', color='skyblue')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.title('Total Sales per Month')
plt.xticks(range(12), month_names, rotation=0)
#### Total Unique Customers per Month
plt.subplot(2, 2, 2)
monthly_unique_customers.plot(kind='bar', color='lightcoral')
plt.xlabel('Month')
plt.ylabel('Total Unique Customers')
plt.title('Total Unique Customers per Month')
plt.xticks(range(12), month_names, rotation=0)
#### Total Transaction Counts per Month
plt.subplot(2, 2, 3)
monthly_transaction_counts.plot(kind='bar', color='lightgreen')
plt.xlabel('Month')
plt.ylabel('Total Transaction Counts')
plt.title('Total Transaction Counts per Month')
plt.xticks(range(12), month_names, rotation=0)
#### Average Product Quality per Month
plt.subplot(2, 2, 4)
monthly_average_quality.plot(kind='bar', color='lightblue')
plt.xlabel('Month')
plt.ylabel('Average Product Quality')
plt.title('Average Product Quality per Month')
plt.xticks(range(12), month_names, rotation=0)
plt.tight_layout()
plt.show()

## 5. General Information
average_sales = merged_data['Total_Sales'].mean()
print(f"Average Sales: {average_sales}")
#### 5.1 Median
median_sales = merged_data['Total_Sales'].median()
print(f"Median Sales: {median_sales}")
#### 5.2 Standard Deviation
std_sales = merged_data['Total_Sales'].std()
print(f"Standard Deviation of Sales: {std_sales}")
#### 5.3 Percentiles
percentile_25 = merged_data['Total_Sales'].quantile(0.25)
percentile_75 = merged_data['Total_Sales'].quantile(0.75)
print(f"25th Percentile: {percentile_25}\n75th Percentile: {percentile_75}")
- The average sales amount is approximately $7.30, indicating the typical sales value across the dataset.
- The median sales value is $7.4, representing the middle point of the sales data, suggesting a balanced distribution.
- The standard deviation of sales is approximately 3.08, signifying the extent of variability or dispersion in sales values. The relatively low standard deviation suggests moderate consistency in sales.

## 6. Correlation
correlation_sales_quality = merged_data['Total_Sales'].corr(merged_data['Product_Quality'])
print(f"Correlation between Sales and Product Quality: {correlation_sales_quality}")
#### 6.1 Correlation between Customer_ID and Transaction_ID
correlation_customer_transaction = merged_data['Customer_ID'].corr(merged_data['Transaction_ID'])
print(f"Correlation between Customer_ID and Transaction_ID: {correlation_customer_transaction}")
#### 6.2 Correlation between Transactions_ID and Total_Sales
correlation_transaction_sales = merged_data['Transaction_ID'].corr(merged_data['Total_Sales'])
print(f"Correlation between Transactions_ID and Total_Sales: {correlation_transaction_sales}")
- There is a strong positive correlation of approximately 0.715 between sales and product quality, suggesting that as product quality improves, sales tend to increase.
- The correlation between customers and transactions is notably high at approximately 0.955, indicating a strong relationship between customers and their transactions.
- In contrast, the correlation between transactions and sales is quite low, around 0.003, suggesting that there is a weak linear relationship between the number of transactions and the total sales amount.


## 7. Type of significance level
lifestage_groups = [
    'YOUNG SINGLES/COUPLES',
    'YOUNG FAMILIES',
    'OLDER SINGLES/COUPLES',
    'MIDAGE SINGLES/COUPLES',
    'NEW FAMILIES',
    'OLDER FAMILIES',
    'RETIREES'
]
#### 7.1 Significance level (alpha)
alpha = 0.05  
#### 7.2 Combinations of lifestage groups for comparison
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

- Rejecting the null hypothesis suggests that certain customer segments have notably different sales patterns, which could be leveraged for tailored marketing campaigns and product offerings.
- The results provide insights into the sales dynamics among different customer groups, helping the business focus on segments with the most potential for revenue growth.
- The findings emphasize the need for customized marketing strategies and product launches to cater to the varying preferences and behaviors of distinct life stage categories.

