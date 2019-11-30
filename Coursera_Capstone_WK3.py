#!/usr/bin/env python
# coding: utf-8

# This is coursera capstone week 3 lab. 

# In[7]:


pip install bs4


# In[8]:


# Library for parsing HTML
from bs4 import BeautifulSoup


# In[12]:


#url
wiki_url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
# Retrieve the html
import requests
canada_html = requests.get(wiki_url).text
#soup_index = BeautifulSoup(index, 'html.parser')


# In[13]:


# Convert to a soup
canada_html = BeautifulSoup(canada_html, 'html.parser')
canada_html


# In[14]:


# Get all the tables
tables = canada_html.find_all('table',class_="wikitable")

# extract the info
contents = [item.get_text() for item in tables[0].find_all('td')]
contents


# In[15]:


# Convert to dataframe with column headers
import pandas as pd
df_head = ['PostalCode', 'Borough', 'Neighbourhood']
df = list(zip(*[iter(contents)]*3))
Toronto_postcodes = pd.DataFrame(df[0:], columns = df_head)
Toronto_postcodes


# In[16]:


#Stripe \n from Neighbourhood
Toronto_postcodes['Neighbourhood'] = Toronto_postcodes['Neighbourhood'].str.rstrip('\n')
Toronto_postcodes


# In[59]:


# Keep only Borough with name
Toronto_postcodes1 = Toronto_postcodes.loc[(Toronto_postcodes.Borough!='Not assigned')]
Toronto_postcodes1


# In[58]:


#Neighbourhood Not assigned
Toronto_postcodes2 = Toronto_postcodes1.loc[Toronto_postcodes1.Neighbourhood=='Not assigned']
Toronto_postcodes2
#one row has Not asssigned, so replacing it with Borough. There must be a efficient way to for it, not sure how...
Toronto_postcodes3 = Toronto_postcodes2.replace({'Neighbourhood': 'Not assigned'}, "Queen's Park")


# In[46]:


#combine data sets
Toronto_df = pd.concat([Toronto_postcodes1,Toronto_postcodes3])
# delete Neighbourhood=Not assigned row
Toronto_df = Toronto_postcodes.loc[(Toronto_postcodes.Neighbourhood!='Not assigned')]
Toronto_df.shape


# In[60]:


path='http://cocl.us/Geospatial_data'
Location_coordinates = pd.read_csv(path)
Location_coordinates.rename(columns={'Postal Code':'PostalCode'},inplace=True)
Location_coordinates


# In[74]:


#comine location coordinates and toronto df to get lat long
neighbourhoods = pd.merge(Toronto_df,Location_coordinates, on = 'PostalCode')
neighbourhoods


# In[48]:


get_ipython().system('conda install -c conda-forge geopy --yes')


# In[66]:


from geopy.geocoders import Nominatim
# Get latitude and longitude values of Toronto
address = 'Toronto, NY'
geolocator = Nominatim(user_agent="tor_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# In[76]:


import folium
# create map of Toronto using latitude and longitude values
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighbourhood in zip(neighbourhoods['Latitude'], neighbourhoods['Longitude'], neighbourhoods['Borough'], neighbourhoods['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# In[69]:





# In[ ]:




