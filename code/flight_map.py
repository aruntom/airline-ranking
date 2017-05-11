import geoplotlib
from pandasql import sqldf
import pandas as pd


df=pd.read_csv('data.csv')
destco=pd.read_csv('destination_latlong.csv')
orgco=pd.read_csv('origin_latlong.csv')
df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%Y-%m-%d')

airline=df.set_index('FL_DATE')


q = """
    SELECT A.ORIGIN_CITY_NAME,A.DEST_CITY_NAME,DC.lat As dlat,DC.lon as dlon,OC.lat As olat,OC.lon as olon FROM airline as A join destco as DC on A.DEST_CITY_NAME=DC.DEST_CITY_NAME join orgco as OC on A.ORIGIN_CITY_NAME=OC.ORIGIN_CITY_NAME WHERE DEP_DELAY=0 AND ARR_DELAY=0;
            
    """
print 'working..'
result=sqldf(q, locals())



geoplotlib.graph(result,
                 src_lat='olat',
                 src_lon='olon',
                 dest_lat='dlat',
                 dest_lon='dlon',
                 color='rainbow',
                 alpha=32,
                 linewidth=2)

geoplotlib.savefig('no delay')
