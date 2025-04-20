%% MATRIX ESTIMATION
%% ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
start_path = 'C:\Moraes\Research\LPR codes\Data';

%Folder with data
directory_name = uigetdir(start_path,'Select directory to open');


%%  Association Matrix Estimation ******************************************
listfile = dir(fullfile(directory_name ,'*lpr*.xls'));

gh_distance = 3; % distance in miles LPR01 - LPR02 
%gh_distance = 12.6; % distance in miles LPR02 - LPR03

z = 9;
min_speed = 35; %mph
max_speed = 90; %mph
dth = 10; %sample time interval at station h (minutes)
gtruth = 'false';
no_sync = 0; %minutes - synchronization correction

% ************************************************************************

prob_type = 1;
day = 1;
for f = day:5 %length(listfile)
display(['File :', listfile(f).name]);
[M,e] = learning(f, z, dth, gh_distance, prob_type, ...
        min_speed, max_speed, no_sync, gtruth, listfile(1:f,:), directory_name);
end
% END^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^













