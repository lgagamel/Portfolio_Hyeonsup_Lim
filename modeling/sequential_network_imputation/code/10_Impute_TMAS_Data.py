# =============================================================================
# Load Library
# =============================================================================
# import os
# import networkx as nx
# import geopandas as gpd
import pandas as pd
# from shapely.geometry import Point, MultiPoint
# from shapely.ops import nearest_points
import numpy as np
# from shapely.ops import nearest_points
# from shapely.geometry import Point, MultiPoint
# import time
# import fiona
# from shapely.geometry import shape
import sys
import time
sys.setrecursionlimit(10000)

df_network = pd.read_csv('output/step_9/0.csv')

# =============================================================================
# nearby links
# =============================================================================
nearby_link_index_list = np.array(["" for x in range(len(df_network))], dtype=object)
for i in range(len(df_network)):
    if i%10000==0:
        print("building nearby_link_index_list...",i)
    Node_O = df_network.iloc[i]["Node_O"]
    Node_D = df_network.iloc[i]["Node_D"]
    
    ind = (df_network["Node_D"]==Node_O)
    ind = ind | (df_network["Node_O"]==Node_D)
    ind = ind & ~((df_network["Node_D"]==Node_O)&(df_network["Node_O"]==Node_D))
    nearby_link_index_list[i] = str([x for x in df_network.loc[ind].index])
    
summary = []
for random_seed in range(100):
    print(random_seed)
    # =============================================================================
    # read data
    # =============================================================================
    df_network = pd.read_csv('output/step_9/'+str(random_seed)+'.csv')
    
    # =============================================================================
    # dummy measure columns
    # =============================================================================
    # for i in range(200):
    #     df_network["dummy_"+str(i)] = df_network["cls_1"]
    
    
    # =============================================================================
    # target measures and wgt column
    # =============================================================================
    target_measure_columns = list(df_network.columns)[df_network.columns.get_loc("cls_5"):df_network.columns.get_loc("cls_13")+1]    
    df_network["cls_6&8"] = df_network["cls_6"]+df_network["cls_8"]
    df_network["cls_10-13"] = df_network["cls_10"]+df_network["cls_12"]+df_network["cls_13"]
    df_network["cls_7&10-13"] = df_network["cls_7"]+df_network["cls_10"]+df_network["cls_12"]+df_network["cls_13"]
    extra_target_columns = ["cls_6&8","cls_10-13","cls_7&10-13"]
    
    # =============================================================================
    # get ratio by class
    # =============================================================================
    df_network[target_measure_columns + extra_target_columns] = np.array(df_network[target_measure_columns + extra_target_columns])/np.array(df_network[target_measure_columns].sum(axis=1)).reshape(-1,1)
    target_measure_columns = target_measure_columns + extra_target_columns
    
    # =============================================================================
    # mark original tmas data
    # =============================================================================
    # df_network["TMAS_ind_original"]=1
    # ind = df_network["TMAS"].isnull()
    # df_network.loc[ind,"TMAS_ind_original"]=0
    # ind = df_network[target_measure_columns].isnull().sum(axis=1)>0
    # df_network.loc[ind,"TMAS_ind_original"]=0
    
    
    # =============================================================================
    # to avoid cases where all the weighting factors are zero
    # =============================================================================
    wgt_column = "HPMS_truck"
    df_network["f"] = df_network[wgt_column] + 0.0001
    
    # =============================================================================
    # make some TMAS null so that we can validate
    # =============================================================================
    df_network_original = df_network.copy()
    # np.random.seed(0)
    # print("TMAS count before",sum(df_network["TMAS_ind_original"]))
    # df_network["TMAS_ind"]=df_network["TMAS_ind_original"]
    # ind = np.random.rand(len(df_network))<0.1
    # df_network.loc[ind,target_measure_columns]=np.nan
    # df_network.loc[ind,"TMAS_ind"]=0
    
    ind_val =  (df_network["TMAS_ind_original"] == 1)&(df_network["TMAS_ind"] == 0)    
    df_network.loc[ind_val,target_measure_columns]=np.nan
    # print("TMAS count after",sum(df_network["TMAS_ind"]))
    
    # =============================================================================
    # nearby links
    # =============================================================================
    # nearby_link_index_list = np.array(["" for x in range(len(df_network))], dtype=object)
    # for i in range(len(df_network)):
    #     if i%10000==0:
    #         print("building nearby_link_index_list...",i)
    #     Node_O = df_network.iloc[i]["Node_O"]
    #     Node_D = df_network.iloc[i]["Node_D"]
        
    #     ind = (df_network["Node_D"]==Node_O)
    #     ind = ind | (df_network["Node_O"]==Node_D)
    #     ind = ind & ~((df_network["Node_D"]==Node_O)&(df_network["Node_O"]==Node_D))
    #     nearby_link_index_list[i] = str([x for x in df_network.loc[ind].index])
    
    # =============================================================================
    # make dataframe to numpy array
    # =============================================================================
    target_measures_array = df_network[target_measure_columns].to_numpy()
    f_array = df_network[["f"]].to_numpy()
    TMAS_ind_array = df_network[["TMAS_ind"]].to_numpy()
    # np.multiply(target_measures_array,f_array)
    # len(np.isnan(target_measures_array[:,1]))
    
    # =============================================================================
    # calculate R-squared
    # =============================================================================
    def get_rsq(actual, predict):
        corr_matrix = np.corrcoef(actual, predict)
        corr = corr_matrix[0,1]
        rsq = corr**2
        return rsq
    
    # =============================================================================
    # Main Loop 
    # =============================================================================
    itr_max = 100
    itr_max_after_no_null = 10
    # print(itr_max)
    n_null = sum(np.isnan(target_measures_array[:,0]))
    rsq = [0 for col in target_measure_columns]
    summary = summary + [[random_seed,0,n_null,0,0]+rsq]
    df_out = df_network.copy()
    n_null_prev = n_null
    itr_after_no_null = 0
    for itr in range(itr_max):
        time_start = time.time()
        
        # check how many estimates are remaining
        delta_sum = 0
        n_null = sum(np.isnan(target_measures_array[:,0]))
        for i in range(len(f_array)):
            #update only if TMAS info is not provided
            if TMAS_ind_array[i]==0:
                nearby_link_index = eval(nearby_link_index_list[i])
                nearby_link_index = nearby_link_index + [i]
                target_measures_array_nearby = target_measures_array[nearby_link_index].copy()
                if np.sum(np.isnan(target_measures_array_nearby)) < target_measures_array_nearby.size:
                    f_array_nearby = f_array[nearby_link_index].copy()
                    f_array_nearby = np.multiply(f_array_nearby,((~np.isnan(target_measures_array_nearby[:,0]))*1).reshape(f_array_nearby.shape))
                    target_measures_array_nearby = np.nan_to_num(target_measures_array_nearby, nan=0)
                    f_array_nearby = np.nan_to_num(f_array_nearby, nan=0)
                    f_array_nearby = f_array_nearby/sum(f_array_nearby)
                    
                    est = np.sum(np.multiply(target_measures_array_nearby,f_array_nearby),axis=0)
                    # est = est/sum(est)
                    if sum(np.isnan(target_measures_array[i]))>0:
                        delta_sum = delta_sum + sum(abs(est))
                    else:
                        delta_sum = delta_sum + sum(np.abs(target_measures_array[i]-est))                    
                    target_measures_array[i] = est
        n_null = sum(np.isnan(target_measures_array[:,0]))
        # df_out = pd.DataFrame(target_measures_array, columns = target_measure_columns)
        df_out[target_measure_columns] = target_measures_array
        tmp_ind_val = ind_val & (df_out[target_measure_columns[0]]>=0)
        n_val = sum(tmp_ind_val)
        rsq = [get_rsq(df_network_original.loc[tmp_ind_val,col], df_out.loc[tmp_ind_val,col]) for col in target_measure_columns]
        summary = summary + [[random_seed,itr+1,n_null,delta_sum,n_val]+rsq]
        # df_out.to_csv("output/step_10/"+str(itr+1)+".csv",index=False)
        time_end = time.time()
        print(random_seed, itr,i,n_null,delta_sum, rsq[8], round(time_end - time_start,2))    
        if n_null_prev == n_null:
            itr_after_no_null = itr_after_no_null + 1
        if itr_after_no_null>=itr_max_after_no_null:
            break
        n_null_prev = n_null

    # =============================================================================
    # output
    # =============================================================================
    df_summary = pd.DataFrame(summary,columns=["random_seed","itr","n_null","delta_sum","n_val"]+target_measure_columns)
    df_summary.to_csv("output/step_10/"+str(random_seed)+".csv",index=False)

# =============================================================================
# output
# =============================================================================
df_summary = pd.DataFrame(summary,columns=["random_seed","itr","n_null","delta_sum","n_val"]+target_measure_columns)
df_summary.to_csv("output/step_10/summary.csv",index=False)


df_out.to_csv("output/step_10/final_est.csv",index=False)
        
