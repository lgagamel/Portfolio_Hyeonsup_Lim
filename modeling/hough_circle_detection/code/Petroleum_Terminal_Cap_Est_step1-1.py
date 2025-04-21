# =============================================================================
# Petroleum_Terminal_Cap_Est_step1-1
# Estimate Capacity from Step 0-2
# =============================================================================


# source: https://developers.google.com/maps/documentation/maps-static/dev-guide

# importing required modules 
import requests 
import pandas as pd
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt	
from scipy.optimize import minimize
from scipy.optimize import Bounds
import cv

#center = "40.714728,-73.998672"

os.chdir(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P1_Capacity')

df_original = pd.read_csv(r'C:\Users\9hl\Dropbox\ORNL\03.Poster\191106_International_Visualization_in_Transportation\Analysis2\P0_Data\p0_capacity.csv')

df = df_original.loc[df_original['TerminalCapacity (barrels)']>0]

def make_folders(dir_list):
    for tmp_dir in dir_list:
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
            
def get_googlemap(center, api_key = "XXXX", zoom = 16, size = "1600x1600", maptype = "satellite"):
    temp_url = "https://maps.googleapis.com/maps/api/staticmap?" 
    temp_url = temp_url + "center=" + center + "&zoom=" + str(zoom) 
    temp_url = temp_url + "&size=" + size + "&maptype=" + maptype 
    temp_url = temp_url + "&key=" + api_key 
    r = requests.get(temp_url)
    return r

def save_googlemap(r, out_fp):
    f = open(out_fp, 'wb') 
    f.write(r.content) 
    f.close()
    
def draw_circles(storage, output):
    circles = np.asarray(storage)
    for circle in circles:
        Radius, x, y = int(circle[0][3]), int(circle[0][0]), int(circle[0][4])
        cv.Circle(output, (x, y), 1, cv.CV_RGB(0, 255, 0), -1, 8, 0)
        cv.Circle(output, (x, y), Radius, cv.CV_RGB(255, 0, 0), 3, 8, 0)
        
def r_squared(y_obs, y_est):    
    y_mean = np.mean(y_obs)
    SS_err = np.sum((y_est - y_obs)**2)
    SS_tot = np.sum((y_mean - y_obs)**2)
    return 1 - (SS_err/SS_tot)


def remove_overlap(output_circles, new_circles, r_mode):        
    new_circles['r-r_mode'] = abs(new_circles['r']-r_mode)
    new_circles = new_circles.sort_values(by='r-r_mode')
    noise_rate = sum((new_circles['r-r_mode']/r_mode)>0.5)/len(new_circles)
    
    for i in range(len(new_circles)):
        tmp_circle = new_circles.iloc[[i]][['x','y','r']]
        if len(output_circles)==0:
            output_circles = output_circles.append(tmp_circle)
        else:
            tmp_output_circles_copy = output_circles.copy()            
            tmp_output_circles_copy['dist'] = ((np.array(tmp_circle['x'])-np.array(tmp_output_circles_copy['x']))**2 + (np.array(tmp_circle['y'])-np.array(tmp_output_circles_copy['y']))**2)**0.5
            no_overlapped = sum((np.array(tmp_circle['r'])+np.array(tmp_output_circles_copy['r'])) > tmp_output_circles_copy['dist'])
            if no_overlapped==0:
                output_circles = output_circles.append(tmp_circle)
    return noise_rate, output_circles

def negative_r_squared_for_petroleum_capacity(tmp_p5_par1, all_radius, y_obs):    
    x_est = np.array([sum(np.array(x)**tmp_p5_par1) for x in all_radius])
    
    # fit values, and mean
    coeffs = np.polyfit(x_est, y_obs, 1)
    p = np.poly1d(coeffs)
    y_est = p(x_est)
    neg_r_squared = -r_squared(y_obs,y_est)
    return neg_r_squared

def find_r_squared_max(init_p5_par1, all_radius, y_obs):    
    bounds = Bounds(0, 3)    
    res = minimize(negative_r_squared_for_petroleum_capacity, init_p5_par1, method='trust-constr', args=(all_radius, y_obs), bounds=bounds)
    return res.x


def main_loop(p3_par1, parameter_set, df, saveimg_ind=False):
    parameter_set[0] = p3_par1
    print('running main loop ...')
    tmp_p2_type = 8
    tmp_p2_par1 = parameter_set[0]/2 # 255 for 6/7
    tmp_p2_par2 = parameter_set[0] # 3 for 6/7
    tmp_p2_par3 = 2 # 2 for 6/7
    
    if saveimg_ind == True:
        for i in range(len(df)):
            tmp_ID = df['ID'].iloc[i]
            tmp_input_fp = tmp_itr + '/p1/' + str(tmp_ID) + '.png'
            
            img = cv2.imread(tmp_input_fp,0)
            img = cv2.medianBlur(img,5)
            
            if tmp_p2_type == 1:
                ret,adj_img = cv2.threshold(img,tmp_p2_par1,tmp_p2_par2,cv2.THRESH_BINARY)
            elif tmp_p2_type == 2:
                ret,adj_img = cv2.threshold(img,tmp_p2_par1,tmp_p2_par2,cv2.THRESH_BINARY_INV)
            elif tmp_p2_type == 3:
                ret,adj_img = cv2.threshold(img,tmp_p2_par1,tmp_p2_par2,cv2.THRESH_TRUNC)
            elif tmp_p2_type == 4:
                ret,adj_img = cv2.threshold(img,tmp_p2_par1,tmp_p2_par2,cv2.THRESH_TOZERO)
            elif tmp_p2_type == 5:
                ret,adj_img = cv2.threshold(img,tmp_p2_par1,tmp_p2_par2,cv2.THRESH_TOZERO_INV)
            elif tmp_p2_type == 6:
                adj_img = cv2.adaptiveThreshold(img,tmp_p2_par1,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,tmp_p2_par2,tmp_p2_par3)
            elif tmp_p2_type == 7:
                adj_img = cv2.adaptiveThreshold(img,tmp_p2_par1,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,tmp_p2_par2,tmp_p2_par3)
            elif tmp_p2_type == 8:
                adj_img = cv2.Canny(img,tmp_p2_par1,tmp_p2_par2)
            else:
                adj_img = img
            
            tmp_output_fp = tmp_itr + '/p2/' + str(tmp_ID) + '.png'
            #adj_img = cv2.cvtColor(adj_img,cv2.COLOR_GRAY2BGR)
            cv2.imwrite(tmp_output_fp, adj_img) 
        
    
    # =============================================================================
    # p3 - detect circles from the adjusted images (parameters for HoughCircles)
    # =============================================================================
    # and
    # =============================================================================
    # p4 - calculate estimated area/volumne of detected circles
    # =============================================================================
    
    # default parameter
    tmp_p3_par1 = parameter_set[0]
    #tmp_p3_par2 = 30
    tmp_p3_par2_max = parameter_set[1]
    tmp_p3_par2_min = parameter_set[2]
    tmp_p3_par3 = 5 # minimum radius
    tmp_p3_par4 = 30 # maximum radius
    tmp_p3_par5 = max(5,tmp_p3_par3)# minimum distance between circles
    tmp_p3_par6 = 1.1 # parameter for dp
    
    
    all_radius = []
    for i in range(len(df)):    
        tmp_ID = df['ID'].iloc[i]    
        #print(tmp_ID)
        tmp_input_fp1 = tmp_itr + '/p1/' + str(tmp_ID) + '.png'
        tmp_input_fp2 = tmp_itr + '/p1/' + str(tmp_ID) + '.png'
        
        img = cv2.imread(tmp_input_fp1)
        adj_img = cv2.imread(tmp_input_fp2,0)
        
        output_circles = pd.DataFrame(columns=['x','y','r'])
        prev_circles = pd.DataFrame(columns=['x','y','r','prev'])
        tmp_p3_par2 = tmp_p3_par2_max
        noise_rate = 0
        while (noise_rate < 0.5) and (tmp_p3_par2>tmp_p3_par2_min):
            
            current_circles = cv2.HoughCircles(adj_img,cv2.HOUGH_GRADIENT,dp=tmp_p3_par6,minDist=tmp_p3_par5,
                                    param1=tmp_p3_par1,param2=tmp_p3_par2,minRadius=tmp_p3_par3,maxRadius=tmp_p3_par4)
            if not(current_circles is None):
                current_circles = pd.DataFrame(current_circles[0,:],columns=['x','y','r']) 
                if len(output_circles) == 0:
                    r_mode = current_circles['r'].mode()[0]
                else:
                    r_mode = output_circles['r'].mode()[0]
                new_circles = current_circles.merge(prev_circles,on=['x','y','r'],how='left')
                new_circles = new_circles.fillna(0)
                new_circles = new_circles.loc[new_circles['prev']==0]
                if len(new_circles)>0:            
                    noise_rate, output_circles = remove_overlap(output_circles, new_circles, r_mode)
                
                prev_circles = current_circles.copy()
                prev_circles['prev'] = 1
                #print(tmp_ID,noise_rate,tmp_p3_par2,len(current_circles))
            tmp_p3_par2 = tmp_p3_par2 - 1
            
                    
        #img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        adj_img = cv2.cvtColor(adj_img,cv2.COLOR_GRAY2BGR)
            
        tmp_output_fp3 = tmp_itr + '/p3/' + str(tmp_ID) + '.png'
        tmp_output_fp4 = tmp_itr + '/p4/' + str(tmp_ID) + '.png'
        
        tmp_radius = [0]
        if len(output_circles) == 0:
            if saveimg_ind == True:
                cv2.imwrite(tmp_output_fp3, adj_img)
                cv2.imwrite(tmp_output_fp4, img)
            tmp_radius = tmp_radius + [0]
        else:            
            for j in range(len(output_circles)):
                # add radius to the tmp_radius list
                tmp_circle = output_circles.iloc[j]                
                tmp_radius = tmp_radius + [tmp_circle[2]]  
                
                if saveimg_ind == True:
                    # draw the outer circle
                    #cv2.circle(adj_img,(tmp_circle['x'],tmp_circle['y']),tmp_circle['r'],(0,255,0),-1)
                    cv2.circle(adj_img,(tmp_circle['x'],tmp_circle['y']),tmp_circle['r'],(0,255,0),2)
                    # draw the center of the circle
                    #cv2.circle(adj_img,(tmp_circle['x'],tmp_circle['y']),2,(0,0,255),3)
                    cv2.circle(adj_img,(tmp_circle['x'],tmp_circle['y']),2,(0,0,255),3)
            if saveimg_ind == True:
                cv2.imwrite(tmp_output_fp3, adj_img)
                #cv2.imwrite(tmp_output_fp4, img)
        all_radius = all_radius + [tmp_radius]
    
    # =============================================================================
    # p5 - find relationship between the estimated area/volumne and the capacity
    # =============================================================================
    # and
    # =============================================================================
    # p6 - calculate the overall performance (R-squared)
    # =============================================================================
    init_p5_par1 = 2
    y_obs = np.array(df['TerminalCapacity (barrels)'])
    optimum_p5_par1 = find_r_squared_max(init_p5_par1, all_radius, y_obs)
    p6_optimum = negative_r_squared_for_petroleum_capacity(optimum_p5_par1, all_radius, y_obs)
    
    est_capacity = np.array([sum(np.array(x)**optimum_p5_par1) for x in all_radius])
    
    df_out = df.copy()
    df_out['est_capacity'] = est_capacity
    print(p6_optimum)
    return p6_optimum, optimum_p5_par1, df_out

def find_main_par_optimum(init_p3_par1, parameter_set, df):    
    bounds = Bounds(290, 310)
    saveimg_ind=False
    res = minimize(main_loop, init_p3_par1, method='trust-constr', args=(parameter_set, df, saveimg_ind), bounds=bounds)
    return res.x


#os.chdir('Output')
tmp_itr = 'itr1'
procedure_list = ['p1','p2','p3','p4','p5','p6','p7']
tmp_dir_list = [(tmp_itr+'\\'+x) for x in procedure_list]
make_folders(tmp_dir_list)

# =============================================================================
# p1 - obtain satellite images from google
# =============================================================================
for i in range(len(df_original)):
    tmp_ID = df_original['ID'].iloc[i]
    tmp_lat = df_original['Latitutde'].iloc[i]
    tmp_lon = df_original['Longitude'].iloc[i]
    tmp_center = str(tmp_lat) + ',' + str(tmp_lon)
    tmp_out_fp = tmp_itr + '/p1/' + str(tmp_ID) + '.png'
    r = get_googlemap(tmp_center, zoom = 17)
    save_googlemap(r, tmp_out_fp)







# =============================================================================
# Find Optimum 
# =============================================================================
#msk = np.random.rand(len(df)) <= 0.5
#train = df[msk]
#validation = df[~msk]
#
parameter_set = [
    300, #0 tmp_p3_par1    
    35, #1 tmp_p3_par2_max
    25 #2 tmp_p3_par2_min
    ]
#init_p3_par1 = 300
#
#result = []
#for p3_par1 in range(290,311):
#    p6_optimum, optimum_p5_par1, df_out = main_loop(p3_par1, parameter_set,df)
#    result = result + [[p3_par1,p6_optimum]]
#
#result = np.array(result)
#np.savetxt('test.csv', result, delimiter=',')
#plt.plot(result[:,0], result[:,1])
    



#optimum_parameter_set = find_main_par_optimum(init_p3_par1, parameter_set, df)

p6_optimum, optimum_p5_par1, df_out = main_loop(305, parameter_set,df_original, saveimg_ind=True)

tmp_df_out=df_out.loc[df_out['TerminalCapacity (barrels)']>0]
tmp_ratio = sum(tmp_df_out['TerminalCapacity (barrels)'])/sum(tmp_df_out['est_capacity'])

df_out['est_capacity_final'] = df_out['est_capacity']*tmp_ratio*(df_out['TerminalCapacity (barrels)']<=0) + df_out['TerminalCapacity (barrels)']*(df_out['TerminalCapacity (barrels)']>0)

df_out[['TerminalCapacity (barrels)','est_capacity','est_capacity_final']]
df_out.to_csv('p1_out.csv')


df_out.est_capacity

#plt.plot(df_out['est_capacity'],df_out['TerminalCapacity (barrels)'],'.')

