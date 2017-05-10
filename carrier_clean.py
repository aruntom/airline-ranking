import pandas as pd
import re

carname=pd.read_csv('carriers.csv')
newcar=[]
for index, row in carname.iterrows():
	print row['CARRIER_NAME']
	newcar.append(re.sub('[^a-zA-Z,. ]', '', row['CARRIER_NAME']))
carname['CNAME']=pd.Series(newcar,index=carname.index)
carname.to_csv('carrier.csv')
