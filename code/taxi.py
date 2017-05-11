from pandasql import sqldf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')



df=pd.read_csv('data.csv')

carname=pd.read_csv('carrier.csv')

df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%m/%d/%Y')

airline=df.set_index('FL_DATE').fillna(0)

   
q = """

    SELECT C.CNAME AS CARRIER,AVG(A.TAXI_IN) AS `MEAN TAXI_IN`,AVG(A.TAXI_OUT) AS `MEAN TAXI_OUT` FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER WHERE A.CANCELLED=0 AND A.AIR_TIME>0 GROUP BY A.CARRIER;
    
    """
print 'working..'
result=sqldf(q, locals()).set_index('CARRIER')


print result

result.plot(kind='barh',stacked=True)
plt.ylabel('CARRIER')
plt.xlabel('TIME in Minutes')
plt.tight_layout()
plt.title('TAXI IN vs OUT')
plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.99,x=0.90)
plt.show()

