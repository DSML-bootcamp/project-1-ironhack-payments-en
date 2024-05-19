## Data Analysis project 
"""Dataset:
Lexique - context 
Cash request - actual information
Fees - actual information """

#Part 1. Let's explore the data and clean it up a bit
import numpy as np
import pandas as pd

#import dataset
cash_request_df = pd.read_csv('project_dataset/extract - cash request - data analyst.csv')
fees_df =pd.read_csv('project_dataset/extract - fees - data analyst - .csv')

#Exploration step
#Cash request
cash_request_df.shape #23970 rows & 16 columns 
cash_request_columns = cash_request_df.columns
cash_request_columns
cash_request_df.nunique()
cash_request_df.info()
pd.isnull(cash_request_df)


#Delete user_id who have a deleted account
cash_request_df= cash_request_df[cash_request_df['user_id']>0]


#Data type cleanup
#convert float to int 
cash_request_df['user_id'] = cash_request_df['user_id'].astype(int)
cash_request_df['deleted_account_id'] = cash_request_df['deleted_account_id'].astype(int)



#convert dates to desire type
#Convert "created_at" into a cohort 
cash_request_df['created_at_month']= cash_request_df['created_at'].dt.month
cash_request_df['created_at_year']= cash_request_df['created_at'].dt.year
cash_request_df['created_at_day']= cash_request_df['created_at'].dt.day
#Concatenate year, months into a single string column
cash_request_df['date_created_at'] = cash_request_df['created_at_year'].astype(str) + '-' + cash_request_df['created_at_month'].astype(str)+ '-' + cash_request_df['created_at_day'].astype(str)
#converting string to datetime
cash_request_df['cohort_date']=pd.to_datetime(cash_request_df['date_created_at'], format='%Y-%m-%d')



# Convert reimbursement date to desire format 
#Extract year, month, and day into separate columns
cash_request_df['year_reimbursement'] = cash_request_df['created_at'].dt.year
cash_request_df['month_reimbursement'] = cash_request_df['created_at'].dt.month
cash_request_df['day_reimbursement'] = cash_request_df['created_at'].dt.day
# Concatenate year, month,olumns into a single string column
cash_request_df['full_date_str_reimbursement_date'] = cash_request_df['year_reimbursement'].astype(str) + '-' + cash_request_df['month_reimbursement'].astype(str) + '-' + cash_request_df['day_reimbursement'].astype(str)
# Convert the concatenated string column to datetime format
cash_request_df['reimbursement_date'] = pd.to_datetime(cash_request_df['full_date_str_reimbursement_date'], format='%Y-%m-%d')

#Cohort based on the first CR received by the user
first_request_dates = cash_request_df.groupby('user_id')['created_at'].min()
cohort_df = pd.DataFrame({'user_id':first_request_dates.index, 'first_request': first_request_dates.values })
cash_request_df= pd.merge(cash_request_df,cohort_df, on='user_id', how='left')

#cohort creation
cash_request_df['first_request']= cash_request_df['first_request'].dt.to_period('M')
cash_request_df

#Choosing the columns to use in analysis 
selected_columns_cash = ['id','amount','status','created_at_date','reimbursement_date','user_id','recovery_status','first_request']
cash_request_ndf= cash_request_df[selected_columns_cash].copy()

#recovery_status cleanup
cash_request_ndf['recovery_status']= cash_request_ndf['recovery_status'].fillna('no_incident')

#data explorations calculations
import seaborn as sns
import matplotlib.pyplot as plt

#summary stats
summary_stats = cash_request_ndf.describe().reset_index()
summary_stats



# Create a boxplot for 'amount'
plt.figure(figsize=(8, 6))
sns.boxplot(x=cash_request_ndf['amount'])
plt.title('Boxplot of Amount')
plt.xlabel('Amount')
plt.ylabel('Frequency')
plt.show()

# Count occurrences of user_id for each cohort_month_year
cohort_counts = cash_request_ndf['user_id'].groupby(cash_request_ndf['first_request']).count().reset_index()

#set the palette 
sns.set_palette("Blues")

# Plot the bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='first_request', y='user_id', data=cohort_counts)
plt.title('Count of User_id by First request')
plt.xlabel('Cohort first request')
plt.ylabel('Count of User_id')
plt.xticks(rotation=45)
plt.show()


#fees exploration
fees_df =pd.read_csv('project_dataset/extract - fees - data analyst - .csv')
fees_df.info()

#fees cleanup 

#rows with no cash_request_id, the cash_request_id is present in the reason column therefore it will be extracted 
fees_df['cash_request_id'].fillna(fees_df['reason'].str.extract(r'(\d+)')[0], inplace=True)

#converting object to int 
fees_df['id']= fees_df['id'].astype(int)
fees_df['cash_request_id'] = fees_df['cash_request_id'].astype(int)

#Choose what columns are usefull for the analysis related to cash request 
selected_columns_fees= ['fee_id','cash_request_id','total_amount']
#fees_ndf= fees_df[selected_columns_fees].copy()
fees_ndf = fees_df[selected_columns_fees].groupby('cash_request_id').sum()
fees_ndf.reset_index()

#EDA calculations 
summary_stats_fees= fees_ndf.describe()
print(summary_stats_fees)

#merge

merge_df = pd.merge(cash_request_ndf,fees_ndf, left_on='id', right_on='cash_request_id', how='left')

 
 #clean up NaN values 
merge_df.fillna(0, inplace=True)
merge_df['amount']= merge_df['amount'].astype(int)
merge_df['total_amount']= merge_df['total_amount'].astype(int)
merge_df.info()
merge_df.to_csv('project_dataset/merge_df.csv')
