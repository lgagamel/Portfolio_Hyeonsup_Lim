# =============================================================================
# Library
# =============================================================================
import os
import pandas as pd
import numpy as np

# =============================================================================
# Working Directory
# =============================================================================
os.chdir(r'C:\Users\9hl\Dropbox\ORNL\12.Python\5.Paper\2101_CV_Data_Fusion\Step2')


# =============================================================================
# Error Distribution Input
# =============================================================================
N = 100

dist_bias_min = -0.5
dist_bias_max = +0.5

dist_std_min = +0.1
dist_std_max = +1

gps_bias_min = -0.5
gps_bias_max = +0.5

gps_cov_min = +0.1
gps_cov_max = +1


#preceding_dist_bias
#preceding_dist_std
#following_dist_bias
#following_dist_std

# =============================================================================
# id
# =============================================================================
df = pd.DataFrame(np.array(range(N))+1,columns=['id'])


# =============================================================================
# preceding_dist_bias & preceding_dist_std
# =============================================================================
df['preceding_dist_bias'] = np.random.uniform(dist_bias_min,dist_bias_max,N)
df['preceding_dist_std'] = np.random.uniform(dist_std_min,dist_std_max,N)


# =============================================================================
# following_dist_bias & following_dist_std
# =============================================================================
df['following_dist_bias'] = np.random.uniform(dist_bias_min,dist_bias_max,N)
df['following_dist_std'] = np.random.uniform(dist_std_min,dist_std_max,N)



# =============================================================================
# gps
# =============================================================================
df['x_bias'] = np.random.uniform(gps_bias_min,gps_bias_max,N)
df['y_bias'] = np.random.uniform(gps_bias_min,gps_bias_max,N)
df['x_cov'] = np.random.uniform(gps_cov_min,gps_cov_max,N)
df['y_cov'] = np.random.uniform(gps_cov_min,gps_cov_max,N)
df['xy_cov'] = 0


# =============================================================================
# Output
# =============================================================================
df.to_csv('output/true_err.csv',index=False)