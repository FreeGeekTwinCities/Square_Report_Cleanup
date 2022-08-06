# This script is intended to be run on the Square .csv export from
# Square Dashboard > Reports > Item Sales > Detailed CSV under export dropdown
# 

import pandas as pd
import sys
from datetime import datetime
# if filepath is passed as argument, use that, otherwise prompt for one
if len(sys.argv) == 2:
    filepath = sys.argv[1]
else:
    filepath = input("Please enter filepath of .csv to summarize: ")

# add validation about csv filetypes only, maybe? 

# Open csv into dataframe(df) using pandas to manipulate
tr = pd.read_csv(filepath, sep=',')


# get rid of currency formatting
tr['Gross Sales'] = tr['Gross Sales'].str.replace('$','')
tr['Gross Sales'] = tr['Gross Sales'].str.replace(' ','')
tr['Gross Sales'] = tr['Gross Sales'].str.replace('(','')
tr['Gross Sales'] = tr['Gross Sales'].str.replace(')','')
tr['Gross Sales'] = tr['Gross Sales'].astype(float)

qtyDict = {}
saleDict = {}

for i in range(len(tr)):

    item =  tr.loc[i,'Item']
    qty = tr.loc[i, 'Qty']
    sale = tr.loc[i, 'Gross Sales']
    monitorYN = (tr.loc[i,'Price Point Name'] == "With Monitor")

    # Parse out desktops with/without monitors
    if (monitorYN & (item == ("DESKTOP"))):
        item = "Desktop With Monitor"
    elif (item=="DESKTOP"):
        item = "Desktop WITHOUT Monitor"
    
    # Parse out citizenship PCs with/without monitors
    if (monitorYN & (item == ("Citizenship PC"))):
        item = "Citizenship PC With Monitor"
    elif (item=="Citizenship PC"):
        item = "Citizenship PC WITHOUT Monitor"    

    # add values to appropriate dict
    if item in qtyDict.keys():
        qtyDict[item] = qtyDict[item] + qty
    else:
        qtyDict[item] = qty

    if item in saleDict.keys():
        saleDict[item] += sale
    else:
        saleDict[item] = sale



summary = pd.DataFrame({'Quantity':pd.Series(qtyDict),'Sales Total':pd.Series(saleDict)})
summary.sort_values(by = 'Quantity')
print(summary)

now = datetime.now()
completeFile = "Completed_" + now.strftime("%d%m%Y_%H%M") + ".csv"
summary.to_csv(completeFile)