import pandas as pd
import numpy as np
import os
import csv



# =============================================================================
# Load basic info
# =============================================================================
inputdir = r'C:\Users\9hl\Dropbox\ORNL\21.Data\07.EC\2017'
list_files = os.listdir(inputdir)

#target_col = ['GEO.id','GEO.id2','GEO.display-label','NAICS.id','NAICS.display-label','EMP','ESTAB','PAYANN','RCPTOT']
#target_col = ['GEO.id2','NAICS.id','EMP','RCPTOT']
target_col = ['COUNTY','NAICS2017','ESTAB','EMP','RCPTOT']
#target_col = ['COUNTY','NAICS2017','RCPTOT']

# =============================================================================
# Read data
# =============================================================================
ec = []
for tmp_file in list_files:
    tmp_inputfile_object = open(inputdir + '\\' + tmp_file,'r')
    data = [l for l in csv.reader(tmp_inputfile_object, quotechar="'", delimiter='|', quoting=csv.QUOTE_ALL, skipinitialspace=True)]
    tmp_ec = pd.DataFrame(data[1:],columns=data[0])
    tmp_ec = tmp_ec.loc[tmp_ec["GEOTYPE"]=="03"]
#    if "GEOTYPE" in tmp_ec.columns:
#        tmp_ec = tmp_ec.loc[tmp_ec["GEOTYPE"]=="02"]
    if "TAXSTAT" in tmp_ec.columns:
        tmp_ec = tmp_ec.loc[tmp_ec["TAXSTAT"]=="00"]
    tmp_ec['COUNTY'] = tmp_ec['ST'] + tmp_ec['COUNTY']
    tmp_ec = tmp_ec[target_col]
    ind = (tmp_ec['RCPTOT']=='0')
    tmp_ec.loc[ind,'RCPTOT'] = ''
    ind = (tmp_ec['RCPTOT']=='')
    #tmp_ec = tmp_ec.loc[~ind]
    print(tmp_file, len(tmp_ec))
    if len(ec)==0:
        ec = tmp_ec
    else:
        ec = ec.append(tmp_ec)
ec.columns = ['ANSI_ST_CO','naics','est','emp','rcptot']
#ec.columns = ['ANSI_ST_CO','naics','rcptot']

ec = ec.drop_duplicates() 

# =============================================================================
# Convert data format
# =============================================================================
ec['ANSI_ST_CO'] = ec['ANSI_ST_CO'].astype(str).apply(lambda x: x.zfill(5))
ec['rcptot'] = pd.to_numeric(ec['rcptot'], errors='coerce')
ec['emp'] = ec['emp'].apply(lambda x: x.replace('(r)',''))
ec['emp'] = ec['emp'].replace({'a':9.5,"b":59.5,"c":174.5,"e":374.5,"f":749.5,"g":1749.5, "h":3749.5,"i":7499.5,"j":17499.5,"k":37499.5,"l":74999.5,"m":150000, "X":np.nan, "S":np.nan})
ec['emp'] = ec['emp'].astype(int)
ec['est'] = ec['est'].astype(int)
ec['emp']= ec['est'] + ec['emp']

# =============================================================================
# # wrtie csv file
# =============================================================================
ec.to_csv('output/step_1/ec_county.csv', index=False)

