import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
#import schedule
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
import datetime as dt


period2 = int(time.time())
period1 = period2 - 16216416000


one_year_div_growth_list = []
three_year_div_growth_list = []
five_year_div_growth_list = []

aristocrats = ['WMT']


for stock in aristocrats:
	url = 'https://finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval=capitalGain%7Cdiv%7Csplit&filter=div&frequency=1d&includeAdjustedClose=true'.format(stock, period1, period2)
	r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

	soup = BeautifulSoup(r.text, 'lxml')

	first_row_list = []
	div_row_list = []



	for tr in soup.find_all('tr'):
		first_row = tr.find('span')
		first_row_list.append(first_row.contents)

	for tr in soup.find_all('tr'):
		rows = tr.find_all('strong')
		each_list = []
		for each in rows:
			each_list += each

		div_row_list.append(each_list)

	first_row_list.pop(0)
	div_row_list.pop(0)

	flat_first_row_list = [item for sublist in first_row_list for item in sublist]
	flat_div_row_list = [item for sublist in div_row_list for item in sublist]


	dividend_data = [flat_first_row_list, flat_div_row_list]
	


	df = pd.DataFrame(dividend_data)
	df1 = df.transpose()
	columns = ['Date', 'Dividend']
	df1.columns = columns
	df1 = df1.iloc[:-1, :]
	

	# CONVERT TO FLOAT, GET SUM FOR EACH YEAR, THEN PLOT
	df1['Dividend'] = df1['Dividend'].astype(float)

	df1['Date'] = pd.to_datetime(df1['Date'], format='%b %d, %Y')
	
	df1 = df1['Dividend'].groupby(df1['Date'].dt.to_period('Y')).sum()
	
	#ADD % CHANGE COLUMN AND CHART GROWTH RATE IN DIVIDEND
	df2 = pd.DataFrame(df1)
	df2['1y % Change'] = df2['Dividend'].pct_change()
	df2 = df2.iloc[:-1, :]
	df2['1y % Change'] = df2['1y % Change'] * 100

	df2.to_csv('/Users/broderickbonelli/Desktop/div_change.csv')
	

	data = pd.read_csv('/Users/broderickbonelli/Desktop/div_change.csv')
	data.reset_index()
	columns = ['Date', 'Dividend', '1y % Change']
	data.columns = columns


	#data for table

	div_growth_last = data['1y % Change'].iloc[-1].round(2)
	div_growth_second_to_last = data['1y % Change'].iloc[-2].round(2)
	div_growth_third_to_last = data['1y % Change'].iloc[-3].round(2)
	div_growth_fourth_to_last = data['1y % Change'].iloc[-4].round(2)
	div_growth_fifth_to_last = data['1y % Change'].iloc[-5].round(2)

	one_year_percent_change = str(div_growth_last.round(2)) + '%'
	three_year_percent_change = (div_growth_last + div_growth_second_to_last + div_growth_third_to_last) / 3
	three_year_percent_change = three_year_percent_change.round(2)
	five_year_percent_change = (div_growth_last + div_growth_second_to_last + div_growth_third_to_last + div_growth_fourth_to_last + div_growth_fifth_to_last) / 5
	five_year_percent_change = five_year_percent_change.round(2)

	#create lists to compile into dataframe
	one_year_div_growth_list.append(div_growth_last)
	three_year_div_growth_list.append(three_year_percent_change)
	five_year_div_growth_list.append(five_year_percent_change)

#compile df
final_list = [aristocrats, one_year_div_growth_list, three_year_div_growth_list, five_year_div_growth_list]
final_df = pd.DataFrame(final_list)
final_df2 = final_df.transpose()

#name columns
final_df2.columns = ['Ticker', '1y Dividend Growth', '3y Avg Dividend Growth', '5y Avg Dividend Growth']

final_df2.to_csv('/Users/broderickbonelli/Desktop/div_growth.csv')



#annual dividend chart

fig, ax = plt.subplots(figsize = (9,4))
fig = sns.barplot(x=data['Date'], y=data['Dividend'], color='#3f616f')

ax.set_xticklabels(labels=data['Date'], rotation=45)
ax.set_title(stock + " Annual Dividends Paid per Share (incl. one time disbursements)")
plt.show()
	

# annual dividend growth rate chart

fig, ax = plt.subplots(figsize = (9,4))
fig = sns.barplot(x=data['Date'], y=data['1y % Change'], color='#3f616f')

ax.set_xticklabels(labels=data['Date'], rotation=45)
ax.set_title(stock + " Dividend Growth Rate")
plt.show()






