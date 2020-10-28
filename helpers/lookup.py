#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import json
import pandas as pd
import time
import urllib.parse

apiKey = ""


# In[3]:


add = pd.read_excel("studentHousing.xlsx")
url = []


# In[4]:


def convertAddress(address, cityState):
    index = address.find(",")
    temp = address[0:index]
    combined = temp + " " + cityState

    
    #combined  = combined.replace(" ", "%20")
    combined = combined.replace(",", "")
    return combined

    


# In[5]:


def getData(address): #get data for a single formatted address
    #getting lat-lon coordinated
    params = {"key": apiKey,"address":address }
    encoded = urllib.parse.urlencode(params,quote_via=urllib.parse.quote)
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params = encoded)
    r.json()
    results = r.json()["results"][0]
    geo = results['geometry']
    location = geo["location"]
    mergedLocation = str(location['lat']) + "," + str(location['lng'])
    toReturn = []
  
    
    
    #getting nearby restaurant names
    
    params = {"key": "apiKey", "location": mergedLocation, "radius": "400", "type":"restaurant"}
    r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json",params)
    json = r.json()
    toReturn.append(json["results"])
    url.append(r.url)




   #if there are >20 restaurants
  
    while "next_page_token" in json:
        pagetoken = str(json["next_page_token"])
        time.sleep(1) #give places api time to make next page valid
        params = {"key": "apiKey", "location": mergedLocation, "radius": "400", "type":"restaurant", "pagetoken": pagetoken}
        
        r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json",params)
        json = r.json()
        toReturn.append(json["results"])
   
    return toReturn
    


# In[6]:


def getPlaceInfo(placeId):
    website = "..."
    phone = "..."
    
    try:
        params = {"key": "apiKey", "place_id": placeId}
        r = requests.get("https://maps.googleapis.com/maps/api/place/details/json",params)
        result = r.json()["result"]
        website = result["website"]
        
    except:
        pass
    
    try:
        phone = result["international_phone_number"]
        
    except:
        pass
    
    return [website, phone]


# In[7]:


def compute(address, cityState, name):
    temp = convertAddress(address, cityState)
    data = getData(temp)
    nearbyNames = []
    for page in data:
        for place in page:
            [website,phone] = getPlaceInfo(place["place_id"])
            
            nearbyNames.append({"name": place["name"],"website": website, "phone": phone , })
    return {"name": name, "address": address, "nearby": nearbyNames}


# In[ ]:





# In[ ]:


final = {}
errors=[]


for index, row in add.iterrows():
    if (index<500):
        name = row["Apartment Name"]
        address = row["Apartment Building"]
        cityState = row["Location"]
        try:
            temp= compute(address, cityState, name)
            final[str(index+2)] = temp
        except:
            temp = convertAddress(address, cityState)
            errors.append([index+2, temp] )
            pass

       
   
   


# In[216]:


errors


# In[127]:


#website, phone number, name, cuisine type


# In[230]:


final


# In[219]:





# In[231]:


temp = json.dumps(final, indent = 2)


# In[232]:


text_file = open("output.txt", "wt")
n = text_file.write(temp)
text_file.close()


# In[ ]:




