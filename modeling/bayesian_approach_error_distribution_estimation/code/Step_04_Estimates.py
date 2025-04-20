# =============================================================================
# Library
# =============================================================================
import numba
from numba import jit
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.stats import norm
from scipy import stats
import time

# =============================================================================
# Input Parameters
# =============================================================================
DIST_VAR = 1
POS_COV = 1


# =============================================================================
# Initial Error Distribution for GPS
# =============================================================================
#pos = np.dstack(POS_RANGE)
dist = multivariate_normal(mean=[0,0], cov=[[POS_COV,0],[0,POS_COV]])
pos_pdf_by_id =[dist for i in range(101)]


# =============================================================================
# Initial Error Distribution for preceding_dist 
# =============================================================================
dist = norm(loc=[0], scale=[DIST_VAR**0.5])
preceding_dist_pdf_by_id =[dist for i in range(101)]


# =============================================================================
# Initial Error Distribution for following_dist 
# =============================================================================
following_dist_pdf_by_id = preceding_dist_pdf_by_id.copy()

# =============================================================================
# Function to update range
# =============================================================================
# @jit(nopython=True)
def update_range(x, y, interval_):
    x_min = x-interval_/2
    x_max = x+interval_/2 + 0.00001
    y_min = y-interval_/2
    y_max = y+interval_/2 + 0.00001
    range_ = np.dstack(np.mgrid[x_min:x_max:(interval_/3), y_min:y_max:(interval_/3)])
    return range_


# =============================================================================
# Function to update learning set
# =============================================================================
def update_learning_set(df, learning_set):
    df['x_err'] = df['x_obs'] - df['x_est']
    df['y_err'] = df['y_obs'] - df['y_est']
    df['preceding_dist_err'] = df['preceding_dist_obs'] - df['preceding_dist_est']
    df['following_dist_err'] = df['following_dist_obs'] - df['following_dist_est']
    
    
    for id_ in df['id'].unique():
        df_ = df.loc[df['id']==id_]
        pos_err_set = df_[['x_err','y_err']].to_numpy()
        preceding_dist_err_set = df_[['preceding_dist_err']].to_numpy()
        following_dist_err_set = df_[['following_dist_err']].to_numpy()
        
        if len(learning_set['pos'][id_])==0:
            learning_set['pos'][id_] = pos_err_set
            learning_set['preceding_dist'][id_] =  preceding_dist_err_set
            learning_set['following_dist'][id_] =  following_dist_err_set
        else:
            learning_set['pos'][id_] =  np.concatenate((learning_set['pos'][id_], pos_err_set))
            learning_set['preceding_dist'][id_] =  np.concatenate((learning_set['preceding_dist'][id_], preceding_dist_err_set))
            learning_set['following_dist'][id_] =  np.concatenate((learning_set['following_dist'][id_], following_dist_err_set))
    return learning_set


# =============================================================================
# Function to update error dist
# =============================================================================
def update_err_dist(df_est_err,learning_set,pos_pdf_by_id,preceding_dist_pdf_by_id,following_dist_pdf_by_id):    
    
    updated_id_list = []
    for id_ in range(101):
        if len(learning_set['pos'][id_])>30:
            updated_id_list = updated_id_list + [id_]
            
            # position xy
            data = learning_set['pos'][id_]
            mean_ = np.mean(data, axis=0)
            cov_ = np.cov(data, rowvar=0)
            cov_[0][1] = 0
            cov_[1][0] = 0
            dist = multivariate_normal(mean=mean_, cov=cov_)
            pos_pdf_by_id[id_] = dist        
            df_est_err.loc[df_est_err['id']==id_,'x_bias_est'] = df_est_err.loc[df_est_err['id']==id_,'x_bias_est']*0.5 + mean_[0]*0.5
            df_est_err.loc[df_est_err['id']==id_,'y_bias_est'] = df_est_err.loc[df_est_err['id']==id_,'y_bias_est']*0.5 + mean_[1]*0.5
            df_est_err.loc[df_est_err['id']==id_,'x_cov_est'] = df_est_err.loc[df_est_err['id']==id_,'x_cov_est']*0.5 + cov_[0][0]*0.5
            df_est_err.loc[df_est_err['id']==id_,'y_cov_est'] = df_est_err.loc[df_est_err['id']==id_,'y_cov_est']*0.5 + cov_[1][1]*0.5
            df_est_err.loc[df_est_err['id']==id_,'xy_cov_est'] = 0
            
            
            # preceding_dist
            data = learning_set['preceding_dist'][id_]
            mean_ = np.mean(data, axis=0)
            std_ = np.std(data)
            dist = norm(loc=mean_, scale=std_)
            preceding_dist_pdf_by_id[id_] = dist
            df_est_err.loc[df_est_err['id']==id_,'preceding_dist_bias_est'] = df_est_err.loc[df_est_err['id']==id_,'preceding_dist_bias_est']*0.5 + mean_[0]*0.5
            df_est_err.loc[df_est_err['id']==id_,'preceding_dist_std_est'] = df_est_err.loc[df_est_err['id']==id_,'preceding_dist_std_est']*0.5 + std_*0.5
            
            
            # following_dist
            data = learning_set['following_dist'][id_]
            mean_ = np.mean(data, axis=0)
            std_ = np.std(data)
            dist = norm(loc=mean_, scale=std_)
            following_dist_pdf_by_id[id_] = dist
            df_est_err.loc[df_est_err['id']==id_,'following_dist_bias_est'] = df_est_err.loc[df_est_err['id']==id_,'following_dist_bias_est']*0.5 + mean_[0]*0.5
            df_est_err.loc[df_est_err['id']==id_,'following_dist_std_est'] = df_est_err.loc[df_est_err['id']==id_,'following_dist_std_est']*0.5 + std_*0.5
    
    df_est_err['x_cov_est'] = df_est_err['x_cov_est']*(1/np.mean(df_est_err['x_cov_est'])) 
    df_est_err['y_cov_est'] = df_est_err['y_cov_est']*(1/np.mean(df_est_err['y_cov_est']))
    df_est_err['xy_cov_est'] = 0 #df_est_err['xy_cov_est']*(0.2/np.mean(df_est_err['xy_cov_est']))
    df_est_err['preceding_dist_std_est'] = df_est_err['preceding_dist_std_est']*(1/np.mean(df_est_err['preceding_dist_std_est']))
    df_est_err['following_dist_std_est'] = df_est_err['following_dist_std_est']*(1/np.mean(df_est_err['following_dist_std_est']))
    for i in range(100):
        obs_ = df_est_err.iloc[i]
        id_ = int(obs_['id'])
        
        mean_ = [obs_['x_bias_est'],obs_['y_bias_est']]
        cov_ = [[obs_['x_cov_est'],obs_['xy_cov_est']],[obs_['xy_cov_est'],obs_['y_cov_est']]]
        pos_pdf_by_id[id_] = multivariate_normal(mean=mean_, cov=cov_)
        
        mean_ = obs_['preceding_dist_bias_est']
        std_ = obs_['preceding_dist_std_est']
        preceding_dist_pdf_by_id[id_] = norm(loc=mean_, scale=std_)
        
        mean_ = obs_['following_dist_bias_est']
        std_ = obs_['following_dist_std_est']
        following_dist_pdf_by_id[id_] = norm(loc=mean_, scale=std_)
    return df_est_err,pos_pdf_by_id,preceding_dist_pdf_by_id,following_dist_pdf_by_id
    

# =============================================================================
# Function to get local optimum
# =============================================================================
# @jit(nopython=True)
def get_local_optimum(obs_,pos_pdf_by_id,preceding_dist_pdf_by_id,following_dist_pdf_by_id):
    max_ = {}
    
    x = 0
    y = 0
    interval_ = 2
    
    # pos_pdf_preceding
    candidate_preceding_x = obs_['preceding_x_est']
    candidate_preceding_y = obs_['preceding_y_est']

    # pos_pdf_following
    candidate_following_x = obs_['following_x_est']
    candidate_following_y = obs_['following_y_est']
    
    while (interval_>=0.01):
        # tmp_logL for pos xy
        candidate_xy = update_range(x, y, interval_)    
        tmp_logL = np.log(pos_pdf_by_id[int(obs_['id'])].pdf(candidate_xy))
        candidate_x = obs_['x_obs'] - candidate_xy[:,:,0]
        candidate_y = obs_['y_obs'] - candidate_xy[:,:,1]
        
        # tmp_logL for preceding_dist
        candidate_preceding_dist = ((candidate_preceding_x - candidate_x)**2 + (candidate_preceding_y - candidate_y)**2)**0.5
        preceding_dist_err = obs_['preceding_dist_obs'] - candidate_preceding_dist
        tmp_logL = tmp_logL + np.reshape(np.log(preceding_dist_pdf_by_id[int(obs_['id'])].pdf(preceding_dist_err.flatten())), tmp_logL.shape)
        
        # tmp_logL for following_dist
        candidate_following_dist = ((candidate_following_x - candidate_x)**2 + (candidate_following_y - candidate_y)**2)**0.5
        following_dist_err = obs_['following_dist_obs'] - candidate_following_dist
        tmp_logL = tmp_logL + np.reshape(np.log(following_dist_pdf_by_id[int(obs_['id'])].pdf(following_dist_err.flatten())), tmp_logL.shape)
        
        # optimum x y
        ind = np.unravel_index(np.argmax(tmp_logL, axis=None), tmp_logL.shape)
        
        x = candidate_xy[ind][0]
        y = candidate_xy[ind][1]
        interval_ = interval_/2
    
    max_ = {}
    max_['x_est'] = obs_['x_obs'] - x
    max_['y_est'] = obs_['y_obs'] - y
    max_['preceding_dist_est'] = ((candidate_preceding_x - max_['x_est'])**2 + (candidate_preceding_y - max_['y_est'])**2)**0.5
    max_['following_dist_est'] = ((candidate_following_x - max_['x_est'])**2 + (candidate_following_y - max_['y_est'])**2)**0.5
    return max_


# =============================================================================
# Function to Estimate
# =============================================================================
def get_local_optimum_main(df,pos_pdf_by_id,preceding_dist_pdf_by_id,following_dist_pdf_by_id):
    df['x_est'] = 0
    df['y_est'] = 0
    df['preceding_dist_est'] = 0
    df['following_dist_est'] = 0

    # added
    df['preceding_x_est'] = df['preceding_x_obs'] - df['preceding_x_bias_est']
    df['preceding_y_est'] = df['preceding_y_obs'] - df['preceding_y_bias_est']
    df['following_x_est'] = df['following_x_obs'] - df['following_x_bias_est']
    df['following_y_est'] = df['following_y_obs'] - df['following_y_bias_est']

    for line_i in range(len(df)):
        obs_ = df.iloc[line_i]        
        max_ = get_local_optimum(obs_,pos_pdf_by_id,preceding_dist_pdf_by_id,following_dist_pdf_by_id)
        df.iloc[line_i, df.columns.get_loc('x_est')] = max_['x_est']
        df.iloc[line_i, df.columns.get_loc('y_est')] = max_['y_est']
        df.iloc[line_i, df.columns.get_loc('preceding_dist_est')] = max_['preceding_dist_est']
        df.iloc[line_i, df.columns.get_loc('following_dist_est')] = max_['following_dist_est']
    
    #df['x_abs'] = np.abs(df['x_est']-df['x_obs'])
    #df['y_abs'] = np.abs(df['y_est']-df['y_obs'])
    #adj_y = sum(df['x_abs'])/sum(df['y_abs'])
    #df['y_est'] = df['y_obs'] + (df['y_est']-df['y_obs'])*adj_y
    df = df[['id', 'precedingId', 'followingId', 'x', 'y','preceding_dist', 'following_dist', 'x_obs', 'y_obs', 'preceding_dist_obs', 'following_dist_obs', 'x_est','y_est', 'preceding_dist_est', 'following_dist_est']]
    return df


# =============================================================================
# Function to get summary
# =============================================================================
def get_summary(df):
    xy_abs = ((df['x'] - df['x_est'])**2 + (df['y'] - df['y_est'])**2)**0.5
    preceding_dist_abs = np.abs(df['preceding_dist_est'] - df['preceding_dist'])
    following_dist_abs = np.abs(df['following_dist_est'] - df['following_dist'])
    xy_abs_obs = ((df['x'] - df['x_obs'])**2 + (df['y'] - df['y_obs'])**2)**0.5
    preceding_dist_abs_obs = np.abs(df['preceding_dist_obs'] - df['preceding_dist'])
    following_dist_abs_obs = np.abs(df['following_dist_obs'] - df['following_dist'])
    return [np.mean(xy_abs),np.mean(preceding_dist_abs),np.mean(following_dist_abs),np.mean(xy_abs_obs),np.mean(preceding_dist_abs_obs),np.mean(following_dist_abs_obs)]

# =============================================================================
# Initial Learning Set 
# =============================================================================
initial_learning_set = {}
initial_learning_set['pos'] =[[] for i in range(101)]
initial_learning_set['preceding_dist'] =[[] for i in range(101)]
initial_learning_set['following_dist'] =[[] for i in range(101)]
learning_set = initial_learning_set.copy()


# =============================================================================
# True Error Distribution to Be Compared
# =============================================================================
df_est_err_initial = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step2\output\true_err.csv')
df_est_err_initial['preceding_dist_bias_est'] = 0
df_est_err_initial['preceding_dist_std_est'] = 1
df_est_err_initial['following_dist_bias_est'] = 0
df_est_err_initial['following_dist_std_est'] = 1
df_est_err_initial['x_bias_est'] = 0
df_est_err_initial['y_bias_est'] = 0
df_est_err_initial['x_cov_est'] = 1
df_est_err_initial['y_cov_est'] = 1
df_est_err_initial['xy_cov_est'] = 0
df_est_err = df_est_err_initial.copy()
    

# =============================================================================
# Main
# =============================================================================
err_summary = []
for i in range(100):
    infile = 'training_'+str(i).zfill(4)+'.csv'
    
    # read df
    print(infile)
    os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step3\output')
    df = pd.read_csv(infile)
    
    # merge df_est_err
    df_error_dist_preceding = df_est_err[['id','x_bias_est','y_bias_est']].copy()
    df_error_dist_following = df_est_err[['id','x_bias_est','y_bias_est']].copy()
    df_error_dist_preceding.columns = ['precedingId','preceding_x_bias_est','preceding_y_bias_est']
    df_error_dist_following.columns = ['followingId','following_x_bias_est','following_y_bias_est']
    df = df.merge(df_error_dist_preceding,on='precedingId',how='left')
    df = df.merge(df_error_dist_following,on='followingId',how='left')
    
    # estimate
    df = get_local_optimum_main(df,pos_pdf_by_id,preceding_dist_pdf_by_id,following_dist_pdf_by_id)
    os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step4\output')
    df.to_csv(infile,index=False)
    
    # compare and summarize the performance 
    tmp_err_summary = get_summary(df)
    err_summary = err_summary + [tmp_err_summary]
    
    # update learning set
    learning_set = update_learning_set(df, learning_set)
    
    # update error distribution
    df_est_err,pos_pdf_by_id,preceding_dist_pdf_by_id,following_dist_pdf_by_id = update_err_dist(df_est_err,learning_set,pos_pdf_by_id,preceding_dist_pdf_by_id,following_dist_pdf_by_id)
    os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step4\output')
    df_est_err.to_csv('est_err_dist_'+str(i).zfill(4)+'.csv',index=False)

os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step4\output')
df_err_summary = pd.DataFrame(err_summary,columns=['xy','preceding_dist','following_dist','xy_obs','preceding_dist_obs','following_dist_obs'])
df_err_summary.to_csv('err_summary.csv')
