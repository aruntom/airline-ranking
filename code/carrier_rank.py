from pandasql import sqldf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import cPickle as pickle
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
result['OPERATED']=(result['TOTAL SCHEDULED']-result['CANCELLED'])
result['RATIO_OP_SCH']=result['OPERATED']/result['TOTAL SCHEDULED']


q2 = """

    SELECT C.CNAME AS CARRIER, SUM(A.DISTANCE) AS DISTANCE, SUM(A.AIR_TIME) AS `FLY TIME`, AVG(A.ARR_DELAY) AS AVG_ARR_DELAY FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER WHERE A.CANCELLED=0 AND A.AIR_TIME>0  GROUP BY A.CARRIER;
    
    """
print 'working..2'

result2=sqldf(q2, locals()).set_index('CARRIER')



result['FLIGHT_SPEED']=60*result2['DISTANCE']/result2['FLY TIME']
result['ARRIVAL_DELAY']=result2['AVG_ARR_DELAY']


q3 = """

    SELECT CARRIER, SUM(TOT) AS `TOTAL FLIGHTS` FROM (SELECT C.CNAME AS CARRIER,A.FL_NUM , COUNT(*) AS TOT FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER GROUP BY A.CARRIER,A.FL_NUM) GROUP BY CARRIER;
    
    """
print 'working..3'
result3=sqldf(q3, locals()).set_index('CARRIER')


total = result3['TOTAL FLIGHTS'].sum()
result['FLIGHTS_VOLUME'] = result3['TOTAL FLIGHTS'].apply(lambda i:(i/float(total)))


q4 = """

    SELECT C.CNAME AS CARRIER,AVG(A.TAXI_IN) AS `MEAN TAXI_IN`,AVG(A.TAXI_OUT) AS `MEAN TAXI_OUT` FROM airline AS A JOIN carname AS C on A.CARRIER=C.CARRIER WHERE A.CANCELLED=0 AND A.AIR_TIME>0 GROUP BY A.CARRIER;
    
    """
print 'working..4'
result4=sqldf(q4, locals()).set_index('CARRIER')

result['TAXI_IN'] = result4['MEAN TAXI_IN'].apply(lambda x:(x/float(60)))
result['TAXI_OUT'] = result4['MEAN TAXI_OUT'].apply(lambda x:(x/float(60)))

result = result.drop('CANCELLED', 1)
result = result.drop('TOTAL SCHEDULED', 1)
result = result.drop('OPERATED', 1)

with open('ranker.pickle', 'wb') as fp:
  pickle.dump(result, fp,1)
print result

print 'result dumped to pickle'
