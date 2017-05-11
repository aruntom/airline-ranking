from pandasql import sqldf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()  


df=pd.read_csv('data.csv')
carname=pd.read_csv('carrier.csv')

df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%m/%d/%Y')

airline=df.set_index('FL_DATE').fillna(0)


q = """
    SELECT C.CNAME AS Cname,AVG(A.WEATHER_DELAY),AVG(A.CARRIER_DELAY),AVG(A.NAS_DELAY),AVG(A.SECURITY_DELAY),AVG(A.LATE_AIRCRAFT_DELAY) FROM airline AS a JOIN carname AS C on A.CARRIER=C.CARRIER GROUP BY A.CARRIER;
            
    """
print 'working..'
result=sqldf(q, locals()).set_index('Cname')




result.columns = ['Avg Weather Delay', 'Avg carrier Delay','Avg NAS Delay','Avg Security Delay','Avg Late Aircraft Delay']

result['tot']=result['Avg Weather Delay']+result['Avg carrier Delay']+result['Avg NAS Delay']+result['Avg Security Delay']+result['Avg Late Aircraft Delay']
nresult=result.sort_values(['tot'], ascending=True)
print nresult
result=nresult.drop('tot', 1)

result.plot(kind='barh', stacked=True)

locs, labels = plt.xticks()
plt.setp(labels, rotation=0)


plt.title('Average Delay by carrier')
plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.94,x=0.89)
plt.ylabel('Carriers')
plt.xlabel('Total Average Delay in minutes')
plt.subplots_adjust(bottom=0.5)
plt.tight_layout()
plt.show()
