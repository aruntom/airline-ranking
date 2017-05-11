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

    SELECT C.CNAME AS Cname, COUNT(*) as `on time` ,sub.TOTAL AS total FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER Join (SELECT CARRIER, COUNT(*) AS TOTAL FROM airline GROUP BY CARRIER) AS sub on A.CARRIER=sub.CARRIER WHERE A.CANCELLED=0 AND A.ARR_DELAY<=0 GROUP BY A.CARRIER;
    
    """
print 'working..'
result=sqldf(q, locals()).set_index('Cname')
result.columns = ['ON TIME', 'TOTAL']

result['% ON TIME']=(result['ON TIME']/result['TOTAL'])*100
nresult=result.sort_values(['% ON TIME'], ascending=True)


print nresult
my_colors = [(x/20.0, x/10.0, 0.50) for x in range(len(nresult))]

ax = nresult[['% ON TIME']].plot(kind='barh',color=my_colors)

locs, labels = plt.xticks()
plt.setp(labels, rotation=0)


for p in ax.patches:
	ax.annotate("%.2f" % p.get_width(), (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10), textcoords='offset points')

ax.legend_.remove()
plt.title('On Time or Early Arrival')
plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.93,x=0.89)
plt.xlabel('Performance (%)')
plt.ylabel('Carriers')
plt.xlim(0,100)
plt.subplots_adjust(bottom=0.5)
plt.tight_layout()
plt.show()

