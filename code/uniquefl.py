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

    SELECT CARRIER, SUM(TOT) AS `TOTAL FLIGHTS` FROM (SELECT C.CNAME AS CARRIER,A.FL_NUM , COUNT(*) AS TOT FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER GROUP BY A.CARRIER,A.FL_NUM) GROUP BY CARRIER;
    
    """
print 'working..'
result=sqldf(q, locals()).set_index('CARRIER')



total = result['TOTAL FLIGHTS'].sum()
result['TOTAL FLIGHTS'] = result['TOTAL FLIGHTS'].apply(lambda x:(x/float(total)))

print result

result.plot(kind='pie',subplots=True,autopct='%1.1f%%',figsize=(8, 8),rot=45)
plt.ylabel('CARRIER',labelpad = 10)
plt.axis('equal')
plt.tight_layout()
plt.title('FLIGHT VOLUME FROM EACH CARRIER')
plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.93,x=0.25)
plt.show()
