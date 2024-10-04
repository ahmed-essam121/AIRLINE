"library"
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 


"import data set"
air_data=pd.read_csv(r"C:\Users\EL-BOSTAN\OneDrive\Desktop\Airline+Passenger+Satisfaction\airline_passenger_satisfaction.csv")


"information of data"
air_data.info()
print("----------------------------------------------------")
air_data.describe()


"clean data"

air_data.isna().sum()
air_data['Arrival Delay'].fillna(air_data['Arrival Delay'].mode(), inplace=True)

# outlaiers

# Calculate Q1 (25th percentile) and Q3 (75th percentile)
# Define a function to detect outliers using IQR
numeric_df = air_data.select_dtypes(include=['int64', 'float64'])
def detect_outliers_iqr(df):
    outliers = pd.DataFrame(columns=numeric_df .columns)
    for column in numeric_df .columns:
        Q1 = numeric_df [column].quantile(0.25)
        Q3 = numeric_df [column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers_in_col = numeric_df [(df[column] < lower_bound) | (numeric_df [column] > upper_bound)][column]
        outliers = pd.concat([outliers, outliers_in_col], axis=1)
    return outliers

# Detect outliers in each column
outliers = detect_outliers_iqr(numeric_df )
print("Outliers in each column:\n", outliers)


"Data visualization"
"""Which percentage of airline passengers are satisfied?
Does it vary by customer type? What about type of travel?"""


# Assuming 'Satisfaction' is a binary column ('Satisfied', 'Dissatisfied')
satisfaction_counts = air_data['Satisfaction'].value_counts(normalize=True) * 100

# Plotting the percentage of satisfied vs dissatisfied
sns.barplot(x=satisfaction_counts.index, y=satisfaction_counts.values)
plt.title('Percentage of Satisfied vs Dissatisfied Passengers')
plt.ylabel('Percentage')
plt.show()


# Bar plot for satisfaction by customer type
sns.countplot(x='Customer Type', hue='Satisfaction', data=air_data)
plt.title('Satisfaction by Customer Type')
plt.ylabel('Count')
plt.show()


"What is the customer profile for a repeating airline passenger?"
# Filter for repeating passengers
repeating_passengers = air_data[air_data['Customer Type'] == 'Returning']

# Plot the distribution of Age for repeating passengers
plt.figure(figsize=(8, 6))
sns.histplot(repeating_passengers['Age'], bins=20, color='green')
plt.title('Age Distribution of Repeating Passengers')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

"""Which factors contribute to customer satisfaction the most? 
What about dissatisfaction?"""

# Bar plot for satisfaction by type of travel
sns.countplot(x='Type of Travel', hue='Satisfaction', data=air_data)
plt.title('Satisfaction by Type of Travel')
plt.ylabel('Count')
plt.show()


#Factors Contributing to Satisfaction
# Correlation matrix of factors contributing to satisfaction
plt.figure(figsize=(10, 8))
correlation_matrix = air_data[[ 'Food and Drink', 'Online Boarding', 'On-board Service','In-flight Service','In-flight Entertainment']].corr()

# Heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Between Factors and Satisfaction')
plt.show()
