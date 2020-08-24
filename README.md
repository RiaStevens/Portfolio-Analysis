# Portfolio-Analysis
## Project Overview
This Python project reads, analyzes and updates one's stock market portfolio. Given a csv containing the ticker, name, industry, average cost, number of shares and dividend yield for each stock in one's portfolio, portfolio_analysis.py will scrape the web (more specifically, money.cnn.com) to obtain the current price of each stock. From there, it will calculate one's equity in each stock, each cost basis and annual dividend, and the percent and value change between the current market value and average cost of each. It will then calculate the portfolio's total annual dividend, overall dividend yield, total cost basis and the total value and percent changes in the portfolio's value. After printing this information to the console using the tabulate library, the data is copied to an excel spreadsheet in the working directory. Finally, the program, using matplotlib, will produce two graphs. The first graph, a nested pie chart, details in the outer loop the diversity of the portfolio between different market sectors, such as Consumer Cyclical or Technology. The inner loop of the pie chart shows the percentage of the portfolio occupied by each stock. The second graph is a double bar graph depicting the change in the market value (note that this is not the same as the personal equity) of each stock as compared to its average cost.

## Libraries Used
The libraries NumPy, random, Matplotlib, Pandas, Requests, BeautifulSoup (bs4) and tabulate were used in the making of this project.

## Sample Input
The input should be a csv file containing the columns ['Ticker', 'Average Cost', 'Shares', 'Dividend Yield' and 'Industry'] in any order. It is also recommended to include a column 'Stock Name' for readability, although this is column is not necessary. One may either build such a csv file from scratch or convert an Excel or other format spreadsheet into csv format. 

### Sample Excel Spreadsheet
![Sample EXCEL Spreadsheet](https://github.com/RiaStevens/Portfolio-Analysis/blob/master/images/input-example.jpg
)

### Sample csv File
![Sample csv file](https://github.com/RiaStevens/Portfolio-Analysis/blob/master/images/input-csv-example.jpg
)

## Sample Output
Four different items which may be considered output are produced by the program.
The first is a tabulate table of the updated data which is printed to the console.
### Sample Tabulate Output
![Sample Tabulate Output](https://github.com/RiaStevens/Portfolio-Analysis/blob/master/images/tabulate-output.jpg
)

The second is an updated Excel spreadsheet saved to the working directory.
### Sample Excel Output
![Sample Excel Output](https://github.com/RiaStevens/Portfolio-Analysis/blob/master/images/excel-output.jpg
)

Third is a nested pie chart depicting the allocation of value in one's portfolio between sectors and individual stocks.
### Sample Pie Chart
![Sample Pie Chart](https://github.com/RiaStevens/Portfolio-Analysis/blob/master/images/pie-output.jpg
)

Fourth is a double bar graph depicting the change in the value of each stock in the portfolio.
### Sample Bar Graph
![Sample Bar Graph](https://github.com/RiaStevens/Portfolio-Analysis/blob/master/images/bar-output.jpg
)

## Next Steps
- Build more graphs to analyze different aspects of the portfolio, such as dividends
- Implement greater exception-handling
