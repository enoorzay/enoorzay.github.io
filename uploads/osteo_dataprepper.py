"""
This file takes the sample file cocultured_umbilical_endo_cells.tsv, 
gets data deemed sig by the PVAL constant, and plots it for each condition
as well as outputting a tsv of sig genes names and folds
""" 

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import math
import sys
import numpy as np

PVAL= 0.01	#Set to 0 if want to look at all samples

data = pd.read_csv('cocultured_umbilical_endo_cells_nometa.tsv',sep='\t')
keys = data.columns.values.tolist()


# Takes panda frame and keys to plot, creates volcano plot data and significant finding table data and returns
def prepData(data,xkey,ykey):

	#Get rid of 0s before we take log
	data[xkey] = data[xkey].fillna(0)
	data[ykey] = data[ykey].fillna(0)
	data[ykey] = data[ykey].apply(lambda x:0 if x<=0 else -math.log10(x))
	
	#Sig test
	if PVAL > 0:
		threshval = -math.log10(PVAL)
	else:
		threshval = math.inf

	#Filter data
	sigdata = data.loc[data[ykey] > threshval]
	nonsigdata= data.loc[data[ykey] <= threshval]

	#Build nonsig series
	trace0= go.Scattergl(
		x = nonsigdata[xkey],
		y=nonsigdata[ykey],
		name="Non significant",
		mode = "markers",
		marker = dict(
			size = 8,
			color = 'rgba(0, 0, 0, .9)',
			line = dict(
			width = 1,

			)
		),
		text=nonsigdata[keys[1]]

	)
	#Build sig series
	trace1= go.Scattergl(
		x = sigdata[xkey],
		y=sigdata[ykey],
		name="Significant",
		mode = "markers",
		marker = dict(
			size = 10,
			color = 'rgba(255, 0, 0, .9)',
			line = dict(
			width = 2,
			)

		),
		text = sigdata[keys[1]]

	)

	#Prepare table data
	folds = sigdata[xkey]
	names = sigdata[keys[1]]

	tabledata = [names,folds]

	print(len(folds), 'passed significance test')

	graphdata = [trace0, trace1]


	return graphdata,tabledata


#Writes  2 column table to outfile of gene names and folds
def makeTable(table,outfile):
	names = table[0]
	folds = table[1]
	sortednames,sortedfolds =  zip(*sorted(zip(names, folds), key=lambda t: abs(t[1])))

	with open (outfile, 'w') as f:
		for i in range(len(sortednames)-1, 0, -1):
			print(sortednames[i], sortedfolds[i], sep='\t', file=f)







#Plot attributes
direct_plot_title ="4"
direct_protein_fold_key = keys[3]
direct_pval_key = keys[4]
direct_plot_file = "direct_fold_pval_scatter.png"
direct_table_file = "sdirect_table.txt"

#Other plot Attribuets
indirect_plot_title ="3"
indirect_protein_fold_key = keys[6]
indirect_pval_key = keys[7]
indirect_plot_file = "indirect_fold_pval_scatter.png"
indirect_table_file = "sindirect_table.txt"


#Prepares output data
direct_graph_data,direct_table_data = prepData(data,direct_protein_fold_key,direct_pval_key)
indirect_graph_data,indirect_table_data = prepData(data,indirect_protein_fold_key,indirect_pval_key)


#Even more plot attributes
direct_layout = dict(title = direct_plot_title,
		yaxis = dict(zeroline = True,
			title = "Log10(P-val)"
			),
		xaxis = dict(zeroline = True,
			title = "Fold Change"
			)
	)
#Graph obj for direct condition
fig1= dict(data=direct_graph_data, layout=direct_layout)



#Repeat for indirect condition
indirect_layout = dict(title = indirect_plot_title,
		yaxis = dict(zeroline = True,
			title = "Log10(P-val)"
			),
		xaxis = dict(zeroline = True,
			title = "Fold Change"
			)
	)
fig2 = dict(data=indirect_graph_data, layout=indirect_layout)


py.iplot(fig1, filename=direct_plot_file)
py.iplot(fig2, filename=indirect_plot_file)


#Make sure theres sig data for table before calling

if len(direct_table_data) > 0:

	makeTable(direct_table_data,direct_table_file)
if len(indirect_table_data) > 0:

	makeTable(indirect_table_data,indirect_table_file)


