#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pylab
get_ipython().run_line_magic('pylab', 'inline')
import pandas as pd
import numpy as np
import seaborn
from datetime import datetime


# In[12]:


data_c = pd.read_csv(r'C:\Python38\anaconda\cab_rides.csv')
data_w = pd.read_csv(r'C:\Python38\anaconda\weather.csv')
data1,data2


# Convert timestamp data to normal date format

# In[14]:


data_c['date'] = pd.to_datetime(data_c['time_stamp']/ 1000, unit = 's') 
data_w['date'] = pd.to_datetime(data_w['time_stamp'], unit = 's')


# In[20]:


#Create a new column by combining location nad date
data_c['location_date'] = data_c['source'].astype('str') + ' - ' + data_c['date'].dt.strftime('%Y-%m-%d').astype('str') + ' - ' + data_c['date'].dt.hour.astype('str')
data_w['location_date'] = data_w['location'].astype('str') + ' - ' + data_w['date'].dt.strftime('%Y-%m-%d').astype('str') + ' - ' + data_w['date'].dt.hour.astype('str')


# In[24]:


data_w


# In[29]:


#data_w = data_w.drop(columns="merged_date")
#data_c = data_c.drop(columns="merged_date")


# In[26]:


data_w


# In[31]:


data_w.index = data_w['location_date']


# In[32]:


data_w


# In[35]:


data_total = data_c.join(data_w, on= ['location_date'], rsuffix ='_w') # Join the car_ride and weather data


# In[36]:


data_total


# In[37]:


data_total.info() # Displays the total columns and their data types with details


# In[43]:


data_total['id'].value_counts()


# In[111]:


#Create a group by grouping the id
group_id = pd.DataFrame(data_total.groupby('id')[['temp','clouds', 'pressure', 'rain', 'humidity', 'wind']].mean())
data_c_w = data_c.join(group_id, on = ['id'])
group_id


# In[112]:


data_c_w['month']=data_c_w['date'].dt.month
data_c_w['hour']=data_c_w['date'].dt.hour 
data_c_w['day'] = data_c_w['date'].dt.strftime('%a')
data_c_w.head()

    


# In[135]:


#Calculate rate per mile
data_c_w['cost_per_mile']= round((data_c_w['price']/data_c_w['distance']),2)


# In[99]:


#Append \mile at the end of the value
#data_c_w['cost_per_mile']= data_c_w['cost_per_mile'].astype(str) + '\mile'



# In[110]:


#data_c_w['cost_per_mile']


# In[121]:


fig , axes = plt.subplots(figsize= (12,12))
axes.plot(data_c_w[data_c_w['cab_type'] == 'Lyft'].groupby('hour').hour.count().index, data_c_w[data_c_w['cab_type'] == 'Lyft'].groupby('hour').hour.count(), label = 'Lyft')
axes.plot(data_c_w[data_c_w['cab_type'] == 'Uber'].groupby('hour').hour.count().index, data_c_w[data_c_w['cab_type'] =='Uber'].groupby('hour').hour.count(), label = 'Uber')
axes.legend()
axes.set(xlabel = 'Hours', ylabel = 'Number of Rides')
axes.set_title('Ride distribution in a single day');
plt.xticks(range(0,24,1))
plt.show()


# In[125]:


#Average price of ride w.r.to service
uber_order =[ 'UberPool', 'UberX', 'UberXL', 'Black','Black SUV','WAV' ]
lyft_order = ['Shared', 'Lyft', 'Lyft XL', 'Lux', 'Lux Black', 'Lux Black XL']
fig, ax = plt.subplots(2,2, figsize = (20,15))
ax1 = seaborn.barplot(x = data_c_w[data_c_w['cab_type'] == 'Uber'].name, y = data_c_w[data_c_w['cab_type'] == 'Uber'].price , ax = ax[0,0], order = uber_order)
ax2 = seaborn.barplot(x = data_c_w[data_c_w['cab_type'] == 'Lyft'].name, y = data_c_w[data_c_w['cab_type'] == 'Lyft'].price , ax = ax[0,1], order = lyft_order)
ax3 = seaborn.barplot(x = data_c_w[data_c_w['cab_type'] == 'Uber'].groupby('name').name.count().index, y = data_c_w[data_c_w['cab_type'] == 'Uber'].groupby('name').name.count(), ax = ax[1,0] ,order = uber_order)
ax4 = seaborn.barplot(x = data_c_w[data_c_w['cab_type'] == 'Lyft'].groupby('name').name.count().index, y = data_c_w[data_c_w['cab_type'] == 'Lyft'].groupby('name').name.count(), ax = ax[1,1],order = lyft_order)
for p in ax1.patches:
    ax1.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
for p in ax2.patches:
    ax2.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points')
ax1.set(xlabel = 'Type of Service', ylabel = 'Average Price')
ax2.set(xlabel = 'Type of Service', ylabel = 'Average Price')
ax3.set(xlabel = 'Type of Service', ylabel = 'Number of Rides')
ax4.set(xlabel = 'Type of Service', ylabel = 'Number of Rides')
ax1.set_title('Uber Average Price by Type of Service')
ax2.set_title('Lyft Average Price by Type of Service')
ax3.set_title('Number of Uber Rides by Type of Service')
ax4.set_title('Number of Lyft Rides by Type of Service')
plt.show()


# In[131]:


#Average cost w.r.to distance 
fig , ax = plt.subplots(figsize = (16,10))
ax.plot(data_c_w[data_c_w['cab_type'] == 'Lyft'].groupby('distance').price.mean().index, data_c_w[data_c_w['cab_type'] == 'Lyft'].groupby('distance')['price'].mean(), label = 'Lyft')
ax.plot(data_c_w[data_c_w['cab_type'] == 'Uber'].groupby('distance').price.mean().index, data_c_w[data_c_w['cab_type'] =='Uber'].groupby('distance').price.mean(), label = 'Uber')
ax.set_title('Average Price by distance', fontsize= 12)
ax.set(xlabel = 'Distance in Miles', ylabel = 'Average Price($)' )
ax.legend()
plt.show()


# In[133]:


#Average price by distance and type of service
fig, ax = plt.subplots(1,2 , figsize = (22,5))
for i,col in enumerate(data_c_w[data_c_w['cab_type'] == 'Uber']['name'].unique()):
    ax[0].plot(data_c_w[data_c_w['name'] == col].groupby('distance').price.mean().index, data_c_w[data_c_w['name'] == col].groupby('distance').price.mean(), label = col)
ax[0].set_title('Uber Average Price by Distance')
ax[0].set(xlabel = 'Distance in Miles', ylabel = 'Average price($)')
ax[0].legend()
for i,col in enumerate(data_c_w[data_c_w['cab_type'] == 'Lyft']['name'].unique()):
    ax[1].plot(data_c_w[ data_c_w['name'] == col].groupby('distance').price.mean().index, data_c_w[ data_c_w['name'] == col].groupby('distance').price.mean(), label = col)
ax[1].set(xlabel = 'Distance in Mile', ylabel = 'Average price in USD')
ax[1].set_title('Lyft Average Price by Distance')
ax[1].legend()
plt.show()


# In[174]:


#Overpriced rides
high_mile_rates = data_c_w[data_c_w['cost_per_mile'] > 80]
high_mile_rates['cab_type'].value_counts()
#overpriced lyft prices
df_l =high_mile_rates[high_mile_rates['cab_type'] == 'Lyft']
df_l.head(10).loc[:,['distance', 'cab_type', 'price', 'surge_multiplier','name','cost_per_mile']]


# In[176]:


#overpriced uber rides
df_u =high_mile_rates[high_mile_rates['cab_type'] == 'Uber']
df_u.head(10).loc[:,['distance', 'cab_type', 'price', 'surge_multiplier','name', 'cost_per_mile']].sort_values(by = 'cost_per_mile', ascending = False).head(20)


# In[182]:


#Prices of various_serivices offered by Uber and Lyft
over_priced_pivot = high_mile_rates[high_mile_rates['cab_type'] == 'Uber'].pivot_table(index = ['name', 'distance', 'price','surge_multiplier'], values = ['id'], aggfunc = len).rename(columns = {'id' : 'Number of rides'})
over_priced_pivot.reset_index(inplace =True)
over_priced_pivot.sort_values(by = ['Number of rides', 'name'], ascending = False).head(15)
                                                                        


# In[ ]:




