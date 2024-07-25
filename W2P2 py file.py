import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# data loading
df = pd.read_csv(r"C:\Users\adria\Documents\GitHub\W8E1\W2P2_solution.py")
#df.info()

print(df.head(50))

#DATA EXPLORATION

#  overview of the dataset's structure
print(df.info())

# Check for any missing values
#print(df.isnull().sum())

# Get summary statistics for numerical columns
print(df.describe())


# Check for missing values in the DataFrame
missing_values = pd.isnull(df)

# Count missing values in each column
missing_counts = missing_values.sum()

# Count columns with missing values
columns_with_missing = missing_counts[missing_counts > 0].count()

# Check if all columns have missing values
all_columns_missing = missing_counts.all()

# Calculate the total number of missing values
total_missing_values = missing_counts.sum()

# Display the results
print("Missing Values in Each Column:\n", missing_counts)
print("\nNumber of Columns with Missing Values:", columns_with_missing)
print("All Columns Have Missing Values:", all_columns_missing)

# Drop rows with missing values in the 'user_id' column
df.dropna(subset=['user_id'], inplace=True)

# Convert 'created_at' column to datetime format
df['created_at'] = pd.to_datetime(df['created_at'])

# Extract year, month, and day into separate columns
df['year'] = df['created_at'].dt.year
df['month'] = df['created_at'].dt.month
#df['day'] = df['created_at'].dt.day

print(df.head(50))

# Concatenate year, month, and day columns into a single string column
df['full_date_str'] = df['year'].astype(str) + '-' + df['month'].astype(str)

# Convert the concatenated string column to datetime format
df['cohort'] = pd.to_datetime(df['full_date_str'], format='%Y-%m')



