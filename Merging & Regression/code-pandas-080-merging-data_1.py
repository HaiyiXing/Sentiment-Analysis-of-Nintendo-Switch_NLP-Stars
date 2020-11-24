# Import packages
import pandas as pd
import numpy as np
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals()) # Shortcut function.
from sklearn.linear_model import LinearRegression
import csv
import json
import matplotlib.pyplot as plot

# Import NTDOY stock price and convert the date strings to `datetime64`.
PRC = pd.read_csv('NTDOY.csv')
PRC['Date'] = pd.to_datetime(PRC['Date'])
PRC = PRC[['Date', 'Share return']] # Just Date and Share return.

# Same for review_new, this is the sentiment score.
review = pd.read_csv('review_new.csv')
review['Datadate'] = pd.to_datetime(review['Datadate'])
review = review[['Datadate', 'Sentiment Score']] # Just Datadate and Sentiment Score.

# We wait for 1 week before using stock return data. 
# The reason is that in real life, it takes time to translate the effects of product review into share price.
review['Datadate'] = review['Datadate'] + np.timedelta64(7, 'D')

# Extract a subset of the data for better illustration of the
# following merge. `PRC` is the stock return and `review` is sentiment score.
PRC = PRC[['Date', 'Share return']]
review = review[['Datadate', 'Sentiment Score']]

# Inspect the data. 
PRC.tail()
review.tail()

# Use SQL syntax to merge the two DataFrames using a left join
# `SELECT *` means to select all columns from the resulting merged data. 
# In the `ON...` part, in order to tell SQL the DataFrame and column it should use, we add the
# DataFrame name in front of the column, separated by a dot. 
# For example, `PRC.Date` means that we are referring to the `Date` column from the `PRC` DataFrame.
df1 = \
    pysqldf(
        'SELECT * ' + \
        'FROM PRC LEFT JOIN review ' + \
        'ON PRC.Date=review.Datadate ' )

# Converts `str` back to `datetime64`
df1['Date'] = pd.to_datetime(df1['Date'])
df1['Datadate'] = pd.to_datetime(df1['Datadate'])

# Make all NaN to zero(int)
df1.fillna(0, inplace=True) 

# Resulting merge, show only 'Date', 'Share return' and 'Sentiment Score'.
df1 = df1[['Date', 'Share return', 'Sentiment Score']] 
print (df1)

# Write results to csv file
df1.to_csv('regression_data.csv', encoding='utf-8', index=False)

# Plot the graph with 'Share return' on x-axis and 'Sentiment Score' on y-axis
df1.plot(x="Share return", y="Sentiment Score", style="o")
plot.title('Regression')
plot.show()

# Calculate the correlation
corre = df1['Sentiment Score'].corr(df1['Share return']) 
print(corre)