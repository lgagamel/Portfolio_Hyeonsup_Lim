# =============================================================================
# Library
# =============================================================================
import os
import pandas as pd
import numpy as np

# =============================================================================
# Working Directory
# =============================================================================
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step1')


for i in range(60):
    i = str(i+1).zfill(2)
    infile = i + '_tracks.csv'
    os.chdir(r'C:\Users\9hl\Dropbox\ORNL\21.Data\11.highD\highd-dataset-v1.0\highD-dataset-v1.0\data')
    df = pd.read_csv(infile)
    df = df[['frame','id','x','y','precedingId','followingId','laneId']]
    df['ind_both'] = 0
    df.loc[(df['precedingId']>0)&(df['followingId']>0),'ind_both'] = 1
    
    
    list_laneId = np.sort(df['laneId'].unique())
    for laneId_ in list_laneId:
        df_ = df.loc[df['laneId']==laneId_]
        os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step1\input')
        df_.to_csv(i+'_'+str(laneId_)+'.csv',index=False)