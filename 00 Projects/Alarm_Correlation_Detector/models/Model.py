#import libs
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import json

#Read Alarms
DATA_PATH = '../data/processed/Alarms_data_processed.parquet'
df = pd.read_parquet(DATA_PATH)

# Encode Function
def encode(x):
        if x <=0:
            return 0
        if x >=1:
            return 1

# MBA on site
def Detector(site_name_input):
    site_name = site_name_input
    snap = df[df['Alarm Source']==site_name].copy()
    snap['q'] = 1
    snap = snap[['Name','Alarm Source','Occurred On (NT)','q']]
    basket = snap.groupby(['Alarm Source','Occurred On (NT)','Name'])['q'].sum().unstack().reset_index().fillna(0).set_index('Occurred On (NT)')
    basket.drop(columns=['Alarm Source'],inplace=True)
    basket_encode = basket.applymap(encode)
    basket_plus = basket_encode[(basket_encode>0).sum(axis=1)>=2]
    freq_pattern = apriori(basket_plus,min_support=0.03,use_colnames=True).sort_values('support',ascending=False).reset_index(drop=True)
    freq_pattern['len'] = freq_pattern['itemsets'].apply(lambda x: len(x))
    data = freq_pattern[freq_pattern['len']>1]
    data['itemsets'] = data['itemsets'].apply(lambda x: ', '.join(list(x))).astype("unicode")
    data_json_process = data.to_json(orient='records',force_ascii=False)
    data_json = json.loads(data_json_process)
    return data_json


#Site alarms Viz
data=[]
snap = df[df['Alarm Source']=='LCAIE12478']
for i in snap['Name'].unique():
    snap2 = snap[snap['Name']==i]
    trace = go.Scatter(x=pd.to_datetime(snap2['Occurred On (NT)']),y=snap2['Name'],name=i,mode='markers')
    data.append(trace)
layout = go.Layout(title='Alarms per time for LCAIE12478', xaxis ={'title':'time'},yaxis={'title':'Alarm'}, hovermode = 'x unified',height=600)
fig = go.Figure(data=data, layout=layout)
fig.show()