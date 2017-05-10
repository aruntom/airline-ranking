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

airline=df.set_index('FL_DATE')


q = """
    SELECT DISTANCE,AVG(DEP_DELAY) AS `Average Departure Delay`,AVG(ARR_DELAY) AS `Average Arrival Delay` FROM airline GROUP BY DISTANCE;
            
    """
print 'working..'
result=sqldf(q, locals())

print result

result_scaled = min_max_scaler.fit_transform(result.fillna(0))
sdf_result = pd.DataFrame(result_scaled)
sdf_result.columns = ['Distance', 'Average Departure Delay','Average Arrival Delay']
sdf_result.plot()
plt.title('Delay vs Distance Trend')
plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.90,x=0.835)
plt.ylabel('Rate of Delay')
plt.xlabel('Distance in Miles')
plt.show()