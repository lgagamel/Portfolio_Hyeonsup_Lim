# =============================================================================
# Library
# =============================================================================
import os
import pandas as pd
import numpy as np
#from os import listdir
#from os.path import isfile, join

# =============================================================================
# Working Directory
# =============================================================================
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step1')


# =============================================================================
# list input files
# =============================================================================
list_infile = os.listdir('input')

first=True
for infile in list_infile:
    print(infile)
    df = pd.read_csv('input/' + infile)
    df_preceding = df.copy()
    df_preceding = df_preceding[['frame','id','x','y']]
    df_preceding.columns = ['frame','precedingId','preceding_x','preceding_y']
    
    df_following = df.copy()
    df_following = df_following[['frame','id','x','y']]
    df_following.columns = ['frame','followingId','following_x','following_y']
    
    df = df.merge(df_preceding,on=['frame','precedingId'],how='left')
    df = df.merge(df_following,on=['frame','followingId'],how='left')
    
    df['preceding_dist'] = ((df['preceding_x']-df['x'])**2 + (df['preceding_y']-df['y'])**2)**0.5
    df['following_dist'] = ((df['following_x']-df['x'])**2 + (df['following_y']-df['y'])**2)**0.5
    df = df.loc[df['ind_both']==1]
    
    df['filename'] = infile    
    df['id'] = np.random.randint(100, size=len(df))+1
    df['precedingId'] = np.random.randint(100, size=len(df))+1
    df['followingId'] = np.random.randint(100, size=len(df))+1
    
    df = df[['id', 'x', 'y', 'precedingId', 'followingId','preceding_x', 'preceding_y', 'following_x', 'following_y','preceding_dist', 'following_dist']]
    if first:
        df.to_csv('output/training.csv',index=False)
        first=False
    else:
        df.to_csv('output/training.csv',index=False, mode='a', header=False)
