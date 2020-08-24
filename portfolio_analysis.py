#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 21:40:24 2020

@author: riastevens
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

pd.set_option('display.max_columns', 500)

df = pd.read_csv('./portfolio.csv', index_col="Ticker", header = 0)

df['Average Cost'] = df['Average Cost'].astype(float)
df['Shares'] = df['Shares'].astype(float)
df['Dividend Yield'] = df['Dividend Yield'].astype(float)

df = df.sort_values(by = ['Industry'])

current_prices = [] #[3,5,2,32,2,5,6,7,3,6,7]
my_equities = [] #[9,3,2,4,5,6,2,2,5,6,23]
number_changes = [] #[34,5,2,124,5,3,2,1,4,5,6]
percent_changes = [] #[24,1,3,45,234,52,14,13,4,4,21]
cost_bases = [] #[13,4,14,5,34,15,6,2,46,2,5]
annual_dividends = []

for ticker in df.index:
    
    url = "https://money.cnn.com/quote/quote.html?symb=" + ticker
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    current_price = soup.find("span", streamformat="ToHundredth").get_text()
    
    current_price = float(current_price)
    current_prices.append(current_price)
    
    shares = df.loc[ticker]["Shares"]
    equity = shares * current_price
    my_equities.append(equity)

    average_cost = df.loc[ticker]["Average Cost"]
    cost_basis = average_cost * shares
    
    number_change = equity - cost_basis
    number_changes.append(number_change)
    
    percent_change = (number_change / cost_basis) * 100
    percent_changes.append(percent_change)
    
    cost_bases.append(cost_basis)
    
    div_yield = df.loc[ticker]['Dividend Yield']
    annual_div = 0
    if div_yield != 0:
        annual_div = (div_yield / 100) * equity
    annual_dividends.append(annual_div)

df.insert(len(df.columns), "Annual Dividend", annual_dividends, True)
df.insert(len(df.columns), "Cost Basis", cost_bases, True)
df.insert(len(df.columns), "Market Value", current_prices, True)
df.insert(len(df.columns), "Equity", my_equities, True) 
df.insert(len(df.columns), "Change ($)", number_changes, True)
df.insert(len(df.columns), "Change (%)", percent_changes, True)

total_div = df['Annual Dividend'].sum()
total_cb = df['Cost Basis'].sum()
total_equity = df['Equity'].sum()
total_change = df['Change ($)'].sum()

overall_div_yield = (total_div / total_equity) * 100
overall_perc_change = (total_change / total_cb) * 100


df.loc['Total'] = ['-','-','-','-',overall_div_yield,total_div,total_cb,'-',total_equity,total_change,overall_perc_change]
# print out the data frame
print(tabulate(df, headers=["Ticker", "Name", "Industry", "Average Cost", "Shares", "Dividend Yield", "Annual Dividend", "Cost Basis", "Market Value", "Equity", "Change ($)", "Change (%)"], floatfmt=".2f"))

# copy the dataframe into an excel sheet
df.to_excel('./updated_portfolio.xlsx')

# display a pie chart with stocks classified by industry

industry_dict = {}

for ticker in df.index:
    if ticker == 'Total':
        continue
    industry = df.loc[ticker]["Industry"]
    equity = df.loc[ticker]["Equity"]
    if industry in industry_dict:
        industry_dict[industry] += equity
    else:
        industry_dict[industry] = equity

industries = list(industry_dict.keys())
industry_equities = list(industry_dict.values())

subgroups = list(df.index.array)
subgroups.pop()
subgroup_values = list(df['Equity'])
subgroup_values.pop()

# create colors for the pie chart
random.seed(24)
colors = []
color_dict = {}
inside_colors = []

for industry in industries:
    r = random.uniform(0.3,0.9)
    g = random.uniform(0.3,0.9)
    b = random.uniform(0.3,0.9)
    color_tuple = (r,g,b)
    colors.append(color_tuple)
    color_dict[industry] = color_tuple
    
for subgroup in subgroups:
    industry = df.loc[subgroup]["Industry"]
    if industry == 'N/A':
        continue
    industry_tuple = color_dict[industry]
    r = industry_tuple[0] * 0.8
    g = industry_tuple[1] * 0.8
    b = industry_tuple[2] * 0.8
    color_tuple = (r,g,b)
    inside_colors.append(color_tuple)

# plot exterior chart
wedgeprops = {'width':.4, 'edgecolor':'white'}
outside = plt.pie(industry_equities, colors=colors, radius = 1.3, labels = industries, autopct = '%1.2f%%', pctdistance = 0.9, startangle = 90, wedgeprops = wedgeprops)

# plot interior chart
wedgeprops = {'width':.5, 'edgecolor':'white'}
inside = plt.pie(subgroup_values, colors = inside_colors, radius = 0.9, labels = subgroups, startangle = 90, labeldistance = 0.75, wedgeprops = wedgeprops)

# display a bar chart depicting average cost vs current market value
fig, ax = plt.subplots(figsize=(7,7))

bar_labels = list(df.index.values)
bar_labels.pop()

bar_avgcost_data = list(df['Average Cost'])
bar_avgcost_data.pop()
bar_mv_data = list(df['Market Value'])
bar_mv_data.pop()

locs = np.arange(len(bar_labels))
bar_width = .35

avgcost_bars = ax.bar(x=(locs - bar_width/2), height=bar_avgcost_data, width=bar_width, label = 'Average Cost')
mv_bars = ax.bar(x=(locs + bar_width/2), height=bar_mv_data, width=bar_width, label = 'Market Value')

ax.set_title('Average Cost vs Current Market Value')
ax.set_xticks(locs)
ax.set_xticklabels(bar_labels)
ax.legend()

# label each bar with percent change
def label_change(leftbars, rightbars):
    if len(leftbars) != len(rightbars):
        raise IndexError("IndexError: Groups of bars are of different lengths")
    for (leftbar, rightbar) in zip(leftbars, rightbars):
        left_bar_height = leftbar.get_height()
        right_bar_height = rightbar.get_height()
        if right_bar_height > left_bar_height:
            bar_height = right_bar_height
        else:
            bar_height = left_bar_height
        percent_change = (right_bar_height - left_bar_height) / left_bar_height
        percent_change *= 100
        ax.annotate('{:.2f}'.format(percent_change) + '%', 
                    xy = (leftbar.get_x() + leftbar.get_width(), bar_height),
                    xytext = (0, 4),
                    textcoords = 'offset points',
                    ha = 'center')
        
label_change(avgcost_bars, mv_bars)

# change the colours of output based on how the stock has performed

plt.show()










