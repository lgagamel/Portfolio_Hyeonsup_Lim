import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os
import itertools
from sklearn.model_selection import RepeatedKFold
import warnings
warnings.filterwarnings("ignore")
import scipy
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from joblib import dump

# =============================================================================
# Load all data from step 3
# =============================================================================
XY_cfs_o = pd.read_csv('output/step_6/XY_cfs_o.csv')

# =============================================================================
# Output folder
# =============================================================================
os.chdir('output/step_7/OLS Linear Regression')



# =============================================================================
# Model sub-function - this is the function needs to be changed by model approach
# =============================================================================
def run_MODEL_sub(X_train,X_test,y_train,y_test, target_measure_max, log_transform_ind):
    model = LinearRegression(positive=True)
    # model = LinearRegression()
    model.fit(X_train, y_train)
    y_est = model.predict(X_test)
    
    if log_transform_ind:
        y_est = np.exp(y_est)
        y_test = np.exp(y_test)
    # else:        
    #     y_est = (y_est>0)*y_est
        #print(sum(y_est<0),sum(y_test<0))
    
    y_est = y_est - 0.0001
    y_test = y_test - 0.0001
    
    y_est = y_est*target_measure_max
    y_test = y_test*target_measure_max
    
    mae = mean_absolute_error(y_est,y_test)
    rmse = mean_squared_error(y_est,y_test)**0.5
    r2 = rsquared(y_est, y_test)
    return mae, rmse, r2, model



# =============================================================================
# Sub-functions
# =============================================================================
def df_to_Xy(df):
    X = df.copy()
    y = X.pop(target_measure)
    X = np.array(X)
    y = np.array(y)
    return X, y

# =============================================================================
# Main function to run model
# =============================================================================



def run_MODEL_main(df, target_measure_max, log_transform_ind):
    rkf = RepeatedKFold(n_splits=4, n_repeats=25, random_state=1)
    X, y = df_to_Xy(df)
    mae_list = []
    rmse_list = []
    r2_list = []
    model_coef_list = []
    for train_index, test_index in rkf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        mae, rmse, r2, model = run_MODEL_sub(X_train,X_test,y_train,y_test, target_measure_max, log_transform_ind)
        mae_list = mae_list + [mae]
        rmse_list = rmse_list + [rmse]
        r2_list = r2_list + [r2]
        model_coef_list = model_coef_list + [[model.intercept_]+list(model.coef_)]
    model_output = {'mae_mean':np.mean(mae_list),
              'mae_std':np.std(mae_list),
              'mae_list':mae_list,
              'rmse_mean':np.mean(rmse_list),
              'rmse_std':np.std(rmse_list),
              'rmse_list':rmse_list,
              'r2_mean':np.mean(r2_list),
              'r2_list':r2_list,
              'model_coef_list':model_coef_list,
              'model_coef_median':np.median(model_coef_list,axis=0),
              'model_coef_mean':np.mean(model_coef_list,axis=0),
              }
    _, _, _, model = run_MODEL_sub(X,X,y,y, target_measure_max, log_transform_ind)
    return model_output, model


# =============================================================================
# Functions to evalute model performance
# =============================================================================
def rsquared(x, y):
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2




    
# =============================================================================
# function to get columns for selected naics
# =============================================================================
def col_by_naics(df, naics_):
    output_col_list = []
    for col in df.columns:
        if ("_" in col) and (col.split("_")[1]==naics_):
            output_col_list = output_col_list + [col]
    return output_col_list


# =============================================================================
# function to get all combinations within a list
# =============================================================================
def all_combination(input_list):
    all_combinations = []
    for r in range(1,len(input_list) + 1):    
        combinations_object = itertools.combinations(input_list, r)
        combinations_list = list(combinations_object)
        for tmp_combinations_list in combinations_list:
            all_combinations = all_combinations + [list(tmp_combinations_list)]
    return all_combinations




# =============================================================================
# Main Loop
# =============================================================================
# run for origin
df_out = []
naics_list = list(XY_cfs_o['naics'].unique())

outputfile_all = open("all.csv","w")
outputfile_summary = open("summary.csv","w")

outputfile_all.write("model,measure,naics,N,log,attr,par,mae,rmse,r2\n")
outputfile_summary.write("model,measure,naics,N,log,attr,par,mae,rmse,r2\n") 

#target_measure = 'value'
model_approach = 'Linear Regression (OLS)'
for target_measure in ['tons','value']:
    df_by_target_measure = XY_cfs_o.copy()
    # df_by_target_measure = df_by_target_measure.loc[df_by_target_measure[target_measure+'_f']!='S']
    df_by_target_measure = df_by_target_measure.loc[df_by_target_measure[target_measure]>0]
    for naics_ in naics_list:
        # select dataset by naics
        df_naics = df_by_target_measure.loc[df_by_target_measure['naics']==naics_]
        N = len(df_naics)
        
        # obtain a set of variable combinations
        naics_col_list = col_by_naics(df_naics, str(naics_))
        naics_col_list_all = all_combination(naics_col_list)
        
        # run for each variable set
        min_mae = np.inf
        max_r2 = -np.inf
        final_model_selection = []
        if len(naics_col_list_all)>0:
            for tmp_attr_list in naics_col_list_all:
                # select temp dataset
                df = df_naics[[target_measure]+tmp_attr_list].copy()
                
                # normalize
                target_measure_max = np.max(df[target_measure])
                for col in [target_measure]+tmp_attr_list:
                    df[col] = (df[col])/np.max(df[col])+0.0001
                
                
    #            target_measure_max = 1
    #            for col in [target_measure]+tmp_attr_list:
    #                df[col] = df[col] + 10e-300
             
                # without log-transform
                log_transform_ind = False
                model_output, model = run_MODEL_main(df, target_measure_max, log_transform_ind)
                
                par_str = [str(np.round(par,3)) for par in model_output['model_coef_median']]
                outputfile_all.write(",".join([str(model_approach),
                                      str(target_measure),                                   
                                      str(naics_),
                                      str(N),
                                      str(log_transform_ind),
                                      '"' + "|".join(tmp_attr_list) + '"',
                                      '"' + "|".join(par_str) + '"',
                                      #str(np.round(model_output['model_coef_median'],3)),
                                      str(np.round(model_output['mae_mean'],3)),
                                      str(np.round(model_output['rmse_mean'],3)),
                                      str(np.round(model_output['r2_mean'],3)),
                                      ])+"\n")
                if model_output['mae_mean'] < min_mae:
                    min_mae = model_output['mae_mean']
                    final_model_selection = {"log_transform":log_transform_ind,
                                   "attributes":tmp_attr_list,
                                   "model_output":model_output,
                                   "model":model}
                #print("log_transform:",log_transform_ind,"tmp_attr_list:",tmp_attr_list, "mae_mean:",model_output['mae_mean'])
                
                # with log-transform
                log_transform_ind = True
                for col in [target_measure]+tmp_attr_list: #for col in [target_measure]: 
                    df[col] = np.log(df[col])
                
                #print(min(df[target_measure]))
                model_output, model = run_MODEL_main(df, target_measure_max, log_transform_ind)
                par_str = [str(np.round(par,3)) for par in model_output['model_coef_median']]
                outputfile_all.write(",".join([str(model_approach),
                                      str(target_measure),                                   
                                      str(naics_),
                                      str(N),
                                      str(log_transform_ind),
                                      '"' + "|".join(tmp_attr_list) + '"',
                                      '"' + "|".join(par_str) + '"',
                                      #str(np.round(model_output['model_coef_median'],3)),
                                      str(np.round(model_output['mae_mean'],3)),
                                      str(np.round(model_output['rmse_mean'],3)),
                                      str(np.round(model_output['r2_mean'],3)),
                                      ])+"\n")
                if model_output['mae_mean'] < min_mae:
                    min_mae = model_output['mae_mean']
                    final_model_selection = {"log_transform":log_transform_ind,
                                   "attributes":tmp_attr_list,
                                   "model_output":model_output,
                                   "model":model}
    
                #print("log_transform:",log_transform_ind,"tmp_attr_list:",tmp_attr_list, "mae_mean:",model_output['mae_mean'])
            
            final_par_str = [str(np.round(par,3)) for par in final_model_selection["model_output"]['model_coef_median']]
            
            print(model_approach,
                  target_measure,
                  naics_,
                  "log_transform:",final_model_selection["log_transform"],
                  "attr_list:",final_model_selection["attributes"], 
                  "model_coef_median:",final_par_str,
                  "rmse:",np.round(final_model_selection["model_output"]['rmse_mean'],2),
                  "mae:",np.round(final_model_selection["model_output"]['mae_mean'],2),
                  "r2:",np.round(final_model_selection["model_output"]['r2_mean'],2))
            
            outputfile_summary.write(",".join([str(model_approach),
                                      str(target_measure),                                   
                                      str(naics_),
                                      str(N),
                                      str(final_model_selection["log_transform"]),
                                      '"' + "|".join(final_model_selection["attributes"]) + '"',
                                      '"' + "|".join(final_par_str) + '"',
                                      #str(np.round(final_model_selection["model_output"]['model_coef_median'],3)),
                                      str(np.round(final_model_selection["model_output"]['mae_mean'],3)),
                                      str(np.round(final_model_selection["model_output"]['rmse_mean'],3)),
                                      str(np.round(final_model_selection["model_output"]['r2_mean'],3)),
                                      ])+"\n")
    
            dump(final_model_selection["model"], 'by_naics/' + str(target_measure)+'_'+str(naics_)+"_model.joblib")
            np.savetxt('by_naics/' + str(target_measure)+'_'+str(naics_)+"_mae.csv", final_model_selection["model_output"]['mae_list'], delimiter=",")
            np.savetxt('by_naics/' + str(target_measure)+'_'+str(naics_)+"_rmse.csv", final_model_selection["model_output"]['rmse_list'], delimiter=",")
            np.savetxt('by_naics/' + str(target_measure)+'_'+str(naics_)+"_r2.csv", final_model_selection["model_output"]['r2_list'], delimiter=",")
            np.savetxt('by_naics/' + str(target_measure)+'_'+str(naics_)+"_coef.csv", final_model_selection["model_output"]['model_coef_list'], delimiter=",")

outputfile_all.close() #to change file access modes
outputfile_summary.close() #to change file access modes
