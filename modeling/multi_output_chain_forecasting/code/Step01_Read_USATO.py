# =============================================================================
# library
# =============================================================================
import pandas as pd
# import os

# =============================================================================
# load data
# =============================================================================
# file_list = os.listdir("input/")

for trade_type in ["Import","Export"]:
    # for i,year in enumerate(list(range(2002,2022+1))):
        # print(trade_type)
    # df = pd.read_csv('input/'+trade_type+'_'+str(year)+'.csv', skiprows=3)
    df = pd.read_csv('input/'+trade_type+'.csv', skiprows=3)
    
    
    # =============================================================================
    # rename columns
    # =============================================================================
    df = df.rename(columns={'Commodity':'HS',
                            # 'Time':'year',
                            'Customs Value (Gen) ($US)':'Value',                                
                            'Value ($US)':'Value',
                            'Quantity 1':'Quantity',
                            'Quantity 1 (Gen)':"Quantity",
                            'Unit Value':'Price',
                            'Customs Unit Value (Gen)':'Price'})
    
    # =============================================================================
    # selected columns
    # =============================================================================
    df = df[["HS","Time","Value"]]
    
    
    # =============================================================================
    # pre-processing
    # =============================================================================
    num_columns = ['Value']
    for col in num_columns:
        df[col] = df[col].apply(lambda x: float(str(x).strip().replace(",","")))
    
    df["HS"] = df["HS"].apply(lambda x: x.strip()[:4])
    df["Year"] = df["Time"].apply(lambda x: x.strip()[-4:])
    df["Month"] = df["Time"].apply(lambda x: x.strip()[:-5])
    Month_to_num = {'January':1,
     'February':2,
     'March':3,
     'April':4,
     'May':5,
     'June':6,
     'July':7,
     'August':8,
     'September':9,
     'October':10,
     'November':11,
     'December':12}
    df["Month"] = df["Month"].replace(Month_to_num)
    
    
    # =============================================================================
    # output
    # =============================================================================
    df = df[["HS","Year","Month","Value"]]
    mode="w"
    header=True
    # if i==0:
    #     mode="w"
    #     header=True
    # else:
    #     mode="a"
    #     header=False
    df.to_csv('output/step1/'+trade_type+'.csv',mode=mode,header=header,index=False)

