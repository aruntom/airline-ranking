import geoplotlib
from geopy import geocoders
from pandasql import sqldf
import pandas as pd
from geopy.exc import GeocoderTimedOut
g = geocoders.GoogleV3(api_key='google_map_api_key_here')
def do_geocode(address):
    try:
        return g.geocode(address, timeout=10)
    except GeocoderTimedOut:
        return do_geocode(address, timeout=10)

df=pd.read_csv('data.csv')
df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%Y-%m-%d')
airline=df.set_index('FL_DATE')


q = """
    SELECT DISTINCT DEST_CITY_NAME FROM airline ;
            
    """
print 'working..'
lalst=[]
lolst=[]

result=sqldf(q, locals())
for index, row in result.iterrows():
    print row['DEST_CITY_NAME']+', USA'

    city = do_geocode(row['DEST_CITY_NAME']+', USA')
    lalst.append(city.latitude)
    lolst.append(city.longitude)
    print city.latitude,city.longitude


result['lat']=pd.Series(lalst).values
result['lon']=pd.Series(lolst).values


print result

result.to_csv('destination_latlong.csv')


