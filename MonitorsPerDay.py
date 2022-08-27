import pandas as pd
import sys
from datetime import datetime

# this is a script to get data on monitor sales per day as a csv file from Square's detailed sales data export.
# to get to the detailed data export:
#     - Square dashboard > Reports > Item sales > Export > Detailed CSV

# what counts as a monitor sale? 
#     - Sale of a monitor a la carte (as indicated by "item" = TV/Monitor)
#     - Inclusion of a monitor in a desktop sale (as indicated by "price point name" = "With monitor")

if len(sys.argv) == 2:
    filepath = sys.argv[1]
else:
    filepath = input("Please enter filepath of .csv to summarize: ")

# add validation about csv filetypes only, maybe? 

# Open csv into dataframe(df) using pandas to manipulate
tr = pd.read_csv(filepath, sep=',')

ud = tr.Date.unique()

# get rid of spaces in column names!!! the worst!!!
tr.columns = tr.columns.str.replace(' ','_')

summary = pd.DataFrame()

summary['Date'] = []
summary['Monitor_Sales'] = []

for i in range(len(ud)):
    count = 0
    date = ud[i]
    for j in range(len(tr)):
        if (tr.loc[j,'Date'] == date):
            if ((tr.loc[j,'Item']=="TV/MONITOR") or (tr.loc[j,'Price_Point_Name'] == "With Monitor")):
                count += 1
    summary.loc[i,'Date'] = datetime.strptime(date, '%m/%d/%Y')
    summary.loc[i,'Monitor_Sales'] = count

summary.sort_values(by = 'Date')
print(summary)

now = datetime.now()
completeFile = "Monitor_Sales,RunOn_" + now.strftime("%d%m%Y") + ".csv"
summary.to_csv(completeFile)