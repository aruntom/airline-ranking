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

    SELECT C.CNAME AS Cname, AVG(A.CRS_ELAPSED_TIME) as `AVG SCHEDULED TIME`,AVG(A.ACTUAL_ELAPSED_TIME) AS `AVG ELAPSED TIME` FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER WHERE A.CANCELLED=0 GROUP BY A.CARRIER;
    
    """
print 'working..'
result=sqldf(q, locals()).set_index('Cname')
result.columns = ['AVG SCHEDULED TIME', 'AVG ELAPSED TIME']




result.plot(kind='barh')

locs, labels = plt.xticks()
plt.setp(labels, rotation=0)

plt.title('AVG SCHEDULED VS AVG ACTUAL ELAPSED TIME')
plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.93,x=0.90)
plt.xlabel('Time in Minutes')
plt.ylabel('Carriers')
#plt.subplots_adjust(bottom=0.5)
plt.tight_layout()
plt.show()

