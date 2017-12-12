DATAPATH = "Video_Games_Sales_as_at_22_Dec_2016.csv"
import pandas as pd
import math
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.plotly as py
import plotly.graph_objs as go

data = pd.read_csv(DATAPATH)
data = data.dropna()  #Drop games without rating data


x = data[['Critic_Score', 'User_Score']] 
y = data[['Global_Sales']]

#split into training and test/validation sets
trainx, testx, trainy, testy = train_test_split(x, y, test_size=0.25, random_state=1)


regression_model = LinearRegression()
regression_model.fit(trainx, trainy)


for idx, col_name in enumerate(trainx.columns):
    print("The coefficient for {} is {}".format(col_name, regression_model.coef_[0][idx]))
	

intercept = regression_model.intercept_[0]

print("Intercept: {}".format(intercept))

#Score
print("R squared value:", regression_model.score(testx, testy))

#Make predictions
prediction = regression_model.predict(testx)

regression_model_mse = mean_squared_error(prediction, testy)
print("Mean square Error: ", regression_model_mse)

print("Average offset of prediction", math.sqrt(regression_model_mse))

#Plot predicted values vs actual
actualtrace = go.Scatter(
    y = testy['Global_Sales'],
	name = "Actual Sales"
)

predictedtrace = go.Scatter(
	y = prediction, 
	name = "Predicted Sales"
)

	
plotdata = [actualtrace,predictedtrace]
layout = dict(title = 'Actual Game Sales vs Predicted Sales from Ratings',
              yaxis = dict(title = 'Sales (millions)'),
              )
fig = dict(data=plotdata,layout = layout)
py.iplot(fig, filename='Actual Game Sales vs Predicted Sales from Ratings')
