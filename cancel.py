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

    SELECT C.CNAME AS CARRIER, COUNT(*) as `Cancelled` ,sub.TOTAL AS total FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER Join (SELECT CARRIER, COUNT(*) AS TOTAL FROM airline GROUP BY CARRIER) AS sub on A.CARRIER=sub.CARRIER WHERE A.CANCELLED=1 GROUP BY A.CARRIER;
    
    """
print 'working..'
result=sqldf(q, locals()).set_index('CARRIER')




result.columns = ['CANCELLED', 'TOTAL SCHEDULED']
result['CANCELLATION RATE']=(result['CANCELLED']/result['TOTAL SCHEDULED'])
nresult=result.sort_values(['CANCELLATION RATE'], ascending=True)


print nresult

fig, axes = plt.subplots(nrows=2, ncols=1)

my_colors1 = [(x/10.0, x/100.0, 0.10) for x in range(len(nresult))]
my_colors2 = [(x/20.0, x/10.0, 0.50) for x in range(len(nresult))]

nresult[['TOTAL SCHEDULED']].plot(ax=axes[0],kind='barh',color=my_colors1)
nresult[['CANCELLATION RATE']].plot(ax=axes[1],kind='barh',color=my_colors2)

locs, labels = plt.xticks()
plt.setp(labels, rotation=0)


fig.suptitle('Total Scheduled vs Cancellation (TEXAS, Jan, 2017)')



plt.ylabel('CARRIER')

plt.subplots_adjust(bottom=0.5)
plt.tight_layout()
plt.show()

