from pandasql import sqldf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import cPickle as pickle

matplotlib.style.use('ggplot')

from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()

with open('ranker.pickle','rb') as fi:
	result = pickle.load(fi)

#print result



col=list(result.columns.values)
ind=result.index.values


result_scaled = min_max_scaler.fit_transform(result)
result = pd.DataFrame(result_scaled)
result.columns=col
result=result.set_index(ind)

for i in result.columns:
	result[i]=result[i]+1

a = result.RATIO_OP_SCH*result.FLIGHT_SPEED*result.FLIGHTS_VOLUME
b = result.ARRIVAL_DELAY*result.TAXI_IN*result.TAXI_OUT
result['SCORE'] = a/(1+b)
result=result.sort_values(['SCORE'],ascending=True)

print result.to_string()

result.to_csv('ranks.csv')

flat=['#e74c3c','#d35400','#e67e22','#f39c12','#f1c40f','#2ecc71','#1abc9c','#16a085', '#3498db','#2980b9','#8e44ad']

ax=result['SCORE'].plot(kind='barh',rot=0,color=flat)
locs, labels = plt.yticks()

for i,p,label in zip(reversed(range(len(labels))),ax.patches,labels):

	ax.annotate("%.2f" % p.get_width(), (p.get_x() + p.get_width(), p.get_y()), xytext=(5, 10), textcoords='offset points')
	ax.annotate("%s" % str(i+1)+'. '+label.get_text(), (p.get_x(), p.get_y()),xytext=(5, 10), textcoords='offset points',color='white')


plt.title('Ranking of Carriers')

plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.93,x=0.115)

plt.xlabel('Score')
ax.set_yticks([])

plt.subplots_adjust(bottom=0.5)
plt.tight_layout()
plt.show()

