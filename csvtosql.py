from pandasql import sqldf
import pandas as pd
import matplotlib.pyplot as plt
carname=pd.read_csv('carrier.csv')
df=pd.read_csv('data.csv')
df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%m/%d/%Y')
airline=df.set_index('FL_DATE')


q = """
    SELECT C.CNAME AS CARRIER,AVG(A.DEP_DELAY) AS `MEAN DEPARTURE DELAY`,AVG(A.ARR_DELAY) AS `MEAN ARRIVAL DELAY` FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER GROUP BY CARRIER ;
            
    """
result=sqldf(q, locals()).set_index('CARRIER')
print result
result.plot(kind='barh',stacked=True)
plt.title('CARRIER ARRIVAL vs DEPARTURE')
plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.94,x=0.91)
plt.ylabel('CARRIERS')
plt.xlabel('DELAY in Minutes')
plt.subplots_adjust(bottom=0.5)
plt.tight_layout()
plt.show()