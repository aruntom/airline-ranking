from pandasql import sqldf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()  


df=pd.read_csv('data.csv')


df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%m/%d/%Y')

airline=df.set_index('FL_DATE').fillna(0)


q = """
    SELECT SUM(WEATHER_DELAY),SUM(CARRIER_DELAY),SUM(NAS_DELAY),SUM(SECURITY_DELAY),SUM(LATE_AIRCRAFT_DELAY) FROM airline;
            
    """
print 'working..'
result=sqldf(q, locals())


result.columns = ['Weather Delay','carrier Delay', 'NAS Delay','Security Delay','Late Aircraft Delay']
print result

rs=result.T.squeeze()
rs.name = "Delays"





rs.plot(kind='pie',subplots=True,autopct='%1.1f%%',figsize=(4, 4),explode=(0, 0.15, 0, 0, 0))

locs, labels = plt.xticks()
plt.setp(labels, rotation=0)
plt.legend()
plt.ylabel('Types of Delays',labelpad = 20)
plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.06,x=0.40)
plt.axis('equal')
plt.tight_layout()
plt.title('Percentage of Delay')
plt.show()