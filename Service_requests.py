#!/usr/bin/env python
# coding: utf-8

# #### Importing required libraries ####

# In[55]:


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# #### Importing the dataset into python ####

# In[2]:


ser_rq_df = pd.read_csv('D:/Puru/Python projects/311_service_requests_2010-present/311_Service_Requests_from_2010_to_Present.csv')
# #### Identifying the shape of the dataset ####

# In[3]:


ser_rq_df.shape

# #### Identifying variables with null values ####

# In[4]:


ser_rq_df.isna().sum()

# In[5]:


# deleting variables with too many null values taking the threshold to be 80% of the total values
limit = len(ser_rq_df) * .80
ser_rq_df = ser_rq_df.dropna(thresh=limit, axis=1)
ser_rq_df.shape

# In[6]:


# deleting entries with no geographical coordinates
ser_rq_df = ser_rq_df.dropna(
    subset=['Latitude', 'Longitude', 'Location', 'X Coordinate (State Plane)', 'Y Coordinate (State Plane)'], axis=0)
ser_rq_df.shape

# In[7]:


# deleting rows with too many null values
ser_rq_df = ser_rq_df.dropna(
    subset=['Incident Address', 'Incident Zip', 'Due Date', 'Street Name', 'Cross Street 1', 'Cross Street 2'], axis=0)
ser_rq_df.shape

# In[8]:


# checking the value in variables to delete variables with irrelevant data
for i in ser_rq_df.columns:
    print(i, ':', ser_rq_df[i].value_counts())
    print('-' * 50)

# In[9]:


# deleting variables with irrelevant data
ser_rq_df = ser_rq_df.drop(
    ['Agency', 'Agency Name', 'Park Facility Name', 'Park Borough', 'Facility Type', 'School Name', 'School Number',
     'School Region', 'School Code', 'School Phone Number', 'School Address', 'School City', 'School State',
     'School Zip', 'School Not Found'], axis=1)
ser_rq_df.shape

# In[10]:


# filling the null values in Descriptor column with "No Access"
ser_rq_df['Descriptor'].fillna(value='No Access', inplace=True)

# In[11]:


# filling the null values in Location Type columns with "Other"
ser_rq_df['Location Type'].fillna(value='Other', inplace=True)

# #### Analyzing and deleting date entries with wrong format ####

# In[12]:


# removing entries with no closing date and resolution action updated date
ser_rq_df = ser_rq_df.dropna(subset=['Closed Date', 'Resolution Action Updated Date'], axis=0)

# In[13]:


# rechecking the null values
ser_rq_df.isna().sum()

# In[14]:


# Converting all entries in Created Date and Closed Date columns into proper date time format
ser_rq_df['Created Date'] = pd.to_datetime(ser_rq_df['Created Date'])
ser_rq_df['Closed Date'] = pd.to_datetime(ser_rq_df['Closed Date'])

# #### City-wise complaint frequency plot ####

# In[ ]:


plt.figure(figsize=(15, 10))
ser_rq_df['City'].value_counts().plot(kind='bar')
plt.xlabel('Number of Complaints')
plt.ylabel('City Names')
plt.title('City-wise complaint frequency plot', color='black', backgroundcolor='silver')
plt.show()

# #### Complaint Concentration across Brooklyn ####

# In[16]:


df_brooklyn = ser_rq_df[ser_rq_df['Borough'] == 'BROOKLYN']

# In[17]:


plt.figure(figsize=(8, 10))
plt.subplots_adjust(hspace=.25, wspace=.25)
plt.subplot(2, 1, 1)
plt.scatter(df_brooklyn['Longitude'], df_brooklyn['Latitude'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Complaint concentration across Brooklyn - Scatter Plot', color='black', backgroundcolor='silver')
plt.subplot(2, 1, 2)
plt.hexbin(df_brooklyn['Longitude'], df_brooklyn['Latitude'])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Complaint concentration across Brooklyn - Hexbin Plot', color='black', backgroundcolor='silver')
plt.show()

# #### Barplot representation of the number of difference complaint types ####

# In[18]:


plt.figure(figsize=(8, 5))
sns.barplot(y=ser_rq_df['Complaint Type'].unique(), x=ser_rq_df['Complaint Type'].value_counts())
plt.title('Complaint types', color='black', backgroundcolor='silver')
plt.xlabel('Number of Complaints')
plt.ylabel('Types of Complaints')
plt.show()

# #### Top 10 types of complaints ####

# In[19]:


comp_type = ser_rq_df['Complaint Type'].value_counts()
comp_type.head(10)

# #### Types of complaints in each City in a separate Dataset ####

# In[20]:


city_wise_comps = ser_rq_df.groupby('City')['Complaint Type'].value_counts().unstack()
city_wise_comps.fillna(value=0, inplace=True)
city_wise_comps = city_wise_comps.astype(int)
city_wise_comps.head()

# #### Finding average response time across complaint types ####

# In[21]:


ser_rq_df['Response Time'] = ser_rq_df['Created Date'] - ser_rq_df['Closed Date']

# In[22]:


for i in ser_rq_df['Complaint Type'].unique():
    print('Average response time for', '\033[1m' + i + '\033[0m', 'is',
          ser_rq_df.groupby('Complaint Type')['Response Time'].get_group(i).mean())

# In[24]:


plt.figure(figsize=(15, 10))
ser_rq_df['City'].value_counts().plot(kind='bar')
plt.xlabel('Number of Complaints')
plt.ylabel('City Names')
plt.title('City-wise complaint frequency plot', color='black', backgroundcolor='silver')
plt.show()

# #### Visualize the major types of complaints in each city ####

# In[58]:


"""n = 1
while n <= 50:
    for i in ser_rq_df['City'].unique():
        plt.figure(figsize=(100, 100))
        plt.rcParams['figure.dpi'] = 200
        plt.subplot(50, 1, n)
        ser_rq_df.groupby('City')['Complaint Type'].get_group(i).value_counts().head().plot(kind='pie',
                                                                                            autopct='%1.1f%%')
        plt.axis('equal')
        plt.title(i)
        n = n + 1"""

# In[ ]:
