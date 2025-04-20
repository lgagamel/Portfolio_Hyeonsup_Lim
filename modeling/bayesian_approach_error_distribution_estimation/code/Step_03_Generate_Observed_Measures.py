# =============================================================================
# Library
# =============================================================================
import os
import pandas as pd
import numpy as np


# =============================================================================
# Working Directory
# =============================================================================
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step3')


# =============================================================================
# Input Data
# =============================================================================
df_error_dist = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step2\output\true_err.csv')


# =============================================================================
# error_dist for preceding vehicle
# =============================================================================
df_error_dist_preceding = df_error_dist.copy()
df_error_dist_preceding = df_error_dist_preceding[['id','x_bias','y_bias','x_cov','y_cov','xy_cov']]
df_error_dist_preceding.columns = ['precedingId','preceding_x_bias','preceding_y_bias','preceding_x_cov','preceding_y_cov','preceding_xy_cov']

# =============================================================================
# error_dist for following vehicle
# =============================================================================
df_error_dist_following = df_error_dist.copy()
df_error_dist_following = df_error_dist_following[['id','x_bias','y_bias','x_cov','y_cov','xy_cov']]
df_error_dist_following.columns = ['followingId','following_x_bias','following_y_bias','following_x_cov','following_y_cov','following_xy_cov']



def get_xy(x_bias,y_bias,x_cov,y_cov,xy_cov):
    mean = [x_bias,y_bias]
    cov = [[x_cov,xy_cov],[xy_cov,y_cov]]
    xy = np.random.multivariate_normal(mean, cov)
    return xy[0], xy[1]

# =============================================================================
# Generate Observed Measures
# =============================================================================
df_all = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step1\output\training.csv')
df_all_ = df_all.copy()
df_all_['x'] = df_all['y']
df_all_['y'] = df_all['x']
df_all_['preceding_x'] = df_all['preceding_y']
df_all_['preceding_y'] = df_all['preceding_x']
df_all_['following_x'] = df_all['following_y']
df_all_['following_y'] = df_all['following_x']
df_all = df_all.append(df_all_)


for i in range(100):
    df = df_all.sample(n=30000)
    if len(df)>0:
        df = df.merge(df_error_dist,on=['id'],how='left')
        df = df.merge(df_error_dist_preceding,on=['precedingId'],how='left')
        df = df.merge(df_error_dist_following,on=['followingId'],how='left')
        
        tmp = pd.DataFrame(df.apply(lambda x: get_xy(x['x_bias'], x['y_bias'], x['x_cov'], x['y_cov'], x['xy_cov']), axis=1),columns=['tmp'])
        df['x_obs'] = df['x'] + tmp['tmp'].apply(lambda x: x[0])
        df['y_obs'] = df['y'] + tmp['tmp'].apply(lambda x: x[1])
        
        tmp = pd.DataFrame(df.apply(lambda x: get_xy(x['preceding_x_bias'], x['preceding_y_bias'], x['preceding_x_cov'], x['preceding_y_cov'], x['preceding_xy_cov']), axis=1),columns=['tmp'])        
        df['preceding_x_obs'] = df['preceding_x'] + tmp['tmp'].apply(lambda x: x[0])
        df['preceding_y_obs'] = df['preceding_y'] + tmp['tmp'].apply(lambda x: x[1])
        
        tmp = pd.DataFrame(df.apply(lambda x: get_xy(x['following_x_bias'], x['following_y_bias'], x['following_x_cov'], x['following_y_cov'], x['following_xy_cov']), axis=1),columns=['tmp'])
        df['following_x_obs'] = df['following_x'] + tmp['tmp'].apply(lambda x: x[0])
        df['following_y_obs'] = df['following_y'] + tmp['tmp'].apply(lambda x: x[1])
        
        df['preceding_dist_obs'] = df['preceding_dist'] + df.apply(lambda x: np.random.normal(x['preceding_dist_bias'], x['preceding_dist_std']),axis=1)
        df['following_dist_obs'] = df['following_dist'] + df.apply(lambda x: np.random.normal(x['following_dist_bias'], x['following_dist_std']),axis=1)
        
        #df = df[['id','precedingId', 'followingId','x_obs', 'y_obs','preceding_x_obs','preceding_y_obs','following_x_obs','following_y_obs','preceding_dist_obs','following_dist_obs']]
        os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step3\output')
        df.to_csv('training_'+str(i).zfill(4)+'.csv',index=False)