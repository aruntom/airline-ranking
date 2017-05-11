from pandasql import sqldf
import pandas as pd
import seaborn as sns

sns.set_palette("bright")
sns.set(style="ticks", color_codes=True)

df=pd.read_csv('data.csv')

carname=pd.read_csv('carrier.csv')

df['FL_DATE'] = pd.to_datetime(df['FL_DATE'], format='%m/%d/%Y')

airline=df.set_index('FL_DATE').fillna(0)

   
q = """

    SELECT C.CNAME AS CARRIER, A.DISTANCE AS DISTANCE, A.AIR_TIME AS `FLY TIME` FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER WHERE A.CANCELLED=0 AND A.AIR_TIME>0;
    
    """
print 'working..'
result=sqldf(q, locals())



result['FLY SPEED']=60*result['DISTANCE']/result['FLY TIME']
nresult=result.sort_values(['FLY SPEED'], ascending=True)


print nresult

ax = sns.violinplot(x="FLY SPEED", y="CARRIER", data=nresult);
sns.despine(trim=True)
ax.set_title('FLIGHT SPEED')
sns.plt.suptitle('Based on flights to and from TEXAS, Jan 2017',fontsize=8, y=0.93,x=0.80)
ax.set(xlabel='SPEED (Miles/Hour)', ylabel='CARRIER')
sns.plt.show()
