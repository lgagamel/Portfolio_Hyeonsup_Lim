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


df_network = pd.read_csv('output/step_8/0.csv')

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
    
for random_seed in range(100):
    # =============================================================================
    # read data
    # =============================================================================
    df_network = pd.read_csv('output/step_8/'+str(random_seed)+'.csv')
    
    
    # =============================================================================
    # make centrodi connector volume to zero
    # =============================================================================
    ind = (df_network["Class"]==50)
    df_network.loc[ind,"TOT_17_All"] = 0
    
    # =============================================================================
    # divide two-way roadway volume by 2
    # =============================================================================
    ind = (df_network["DIR"]==0)
    df_network.loc[ind,"TOT_17_All"] = df_network.loc[ind,"TOT_17_All"]/2
    
    
    # =============================================================================
    # dummy measure columns
    # =============================================================================
    # for i in range(200):
    #     df_network["dummy_"+str(i)] = df_network["cls_1"]
    
    
    # =============================================================================
    # make ratio of hpms/faf
    # =============================================================================
    # df_network["HPMS_ind"] = 1
    df_network["HPMS_truck"] = df_network["HPMS_COMBI"] + df_network["HPMS_SINGL"]
    # df_network["HPMS_ratio"] = df_network["HPMS_truck"]/df_network["TOT_17_All"]
    # ind = np.isnan(df_network["HPMS_ratio"])|np.isinf(df_network["HPMS_ratio"])|(df_network["HPMS_ratio"]==0)
    # df_network.loc[ind,"HPMS_ratio"] = np.nan
    # df_network.loc[ind,"HPMS_ind"] = 0
    
    df_network["HPMS_ind"] = 0
    ind = df_network["HPMS_truck"] > 0
    df_network.loc[ind,"HPMS_ind"] = 1
    df_network.loc[~ind,"HPMS_truck"] = np.nan
    
    
    # =============================================================================
    # target measures and wgt column
    # =============================================================================
    target_measure_columns = ["HPMS_truck"] #list(df_network.columns)[df_network.columns.get_loc("cls_1"):]
    
    
    # =============================================================================
    # to avoid cases where all the weighting factors are zero
    # =============================================================================
    wgt_column = "TOT_17_All"
    df_network["f"] = df_network[wgt_column] + 0.0001
    df_network_original = df_network.copy()
    
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
    HPMS_ind_array = df_network[["HPMS_ind"]].to_numpy()
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
    print(itr_max)
    summary = []
    n_null = sum(np.isnan(target_measures_array[:,0]))
    # rsq = [0 for col in target_measure_columns]
    summary = summary + [[0,n_null,0]]
    df_out = df_network.copy()
    n_null_prev = n_null
    itr_after_no_null = 0
    for itr in range(itr_max):
        time_start = time.time()
        
        # check how many estimates are remaining
        delta_sum = 0    
        for i in range(len(f_array)):
            #update only if TMAS info is not provided
            if HPMS_ind_array[i]==0:
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
        # df_out[target_measure_columns] = target_measures_array
        # tmp_ind_val = ind_val & (df_out[target_measure_columns[0]]>=0)
        # n_val = sum(tmp_ind_val)
        # rsq = [get_rsq(df_network_original.loc[tmp_ind_val,col], df_out.loc[tmp_ind_val,col]) for col in target_measure_columns]
        # summary = summary + [[itr+1,n_null,delta_sum,n_val]+rsq]
        summary = summary + [[itr+1,n_null,delta_sum]]
        # df_out.to_csv("output/step_9/"+str(itr+1)+".csv",index=False)
        time_end = time.time()    
        print(random_seed,itr,i,n_null,delta_sum, round(time_end - time_start,2))    
        
        if n_null_prev == n_null:
            itr_after_no_null = itr_after_no_null + 1
        if itr_after_no_null>=itr_max_after_no_null:
            break
        n_null_prev = n_null
    
    # =============================================================================
    # output
    # =============================================================================
    df_out[target_measure_columns] = target_measures_array
    # df_summary = pd.DataFrame(summary,columns=["itr","n_null","delta_sum"])
    # df_summary.to_csv("output/step_9/summary.csv",index=False)
    df_out.to_csv("output/step_9/"+str(random_seed)+".csv",index=False)
            
