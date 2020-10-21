# including converting coordinate to community
# 
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

# data
ca = gpd.read_file('Boundaries - Community Areas (current).geojson')
data = pd.read_csv('raw_data.csv')
print(data.columns)


# --create a community dict with geo information
ca_dict=dict()
ca_name = ca['community']
ca_geo = ca['geometry']
for i in range(len(ca_name)):
    ca_dict[ca_name[i]] = ca_geo[i]

def drop_duplicate(data,col):
    # drop records with duplicate id (subset = id)
    df = data.drop_duplicates(subset=[col])
    return df

def drop_missing(data,col):
    #clean missing value in longitude and latitude
    df = data.dropna(subset=[col])
    return df
    
#define a method to match point and community
def check_ca(long,lat,ca_dict):
    point = Point(long,lat) # Point() should be Point(longitude, latitude)
    for geo in ca_dict:
        if point.within(ca_dict[geo]):
            return geo


def clean_data(data):
    data=data.dropna(subset=['coordinates'])
    # get first category
    data['Category'] = data.apply(lambda x: x['categories'][1],axis=1)
    # get commmunity name
    # data['Community'] = data.apply(lambda x: check_ca(x['longitude'], x['latitude'], ca_dict))
    # data = data.dropna(subset=['Community'])
    return data




clean_df = drop_duplicate(data, 'id')
clean_df = clean_data(clean_df)
print(clean_df.info())