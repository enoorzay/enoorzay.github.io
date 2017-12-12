DATAPATH = "Video_Games_Sales_as_at_22_Dec_2016.csv"
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go


data = pd.read_csv(DATAPATH)

platforms = list(set(data['Platform']))

na = [0 for x in range(0, len(platforms))]
jp =  [0 for x in range(0, len(platforms))]
eu =  [0 for x in range(0, len(platforms))]
other =  [0 for x in range(0, len(platforms))]
for i, j in enumerate(platforms):
	curr = data.loc[data['Platform'] == j]
	na[i] = sum(curr['NA_Sales'])
	jp[i] = sum(curr['JP_Sales'])
	eu[i] = sum(curr['EU_Sales'])
	other[i] = sum(curr['Other_Sales'])

	
NA_Sales = {
  'x': platforms,
  'y': na,
  'name': 'NA Sales',
  'type': 'bar'
};
EU_Sales = {
  'x': platforms,
  'y': eu,
  'name': 'EU Sales',
  'type': 'bar'
};
JP_Sales = {
  'x': platforms,
  'y': jp,
  'name': 'JP Sales',
  'type': 'bar'
 }
 
Other_Sales = {
  'x': platforms,
  'y': other,
  'name': 'Other',
  'type': 'bar'
 }

plotdata = [NA_Sales, EU_Sales, JP_Sales, Other_Sales];
layout = {
  'xaxis': {'title': 'Platform'},
  'yaxis': {'title': 'Game Sales (in millions)'},
  'barmode': 'relative',
  'title': 'Game sales per Platform'
  
};
py.iplot({'data': plotdata, 'layout': layout}, filename='Platform Sales')
