function [] = learning_main(input_folder, matrix_folder,...
        min_speed, max_speed, gh_distance, z_value, gtruth)
%% MATRIX ESTIMATION
%% ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
%%start_path = 'C:\Moraes\Research\LPR codes\Data';

%Folder with data
%%directory_name = uigetdir(start_path,'Select directory to open');
directory_name = input_folder;


%%  Association Matrix Estimation ******************************************
listfile = dir(fullfile(directory_name ,'*lpr*.*'));

%%gh_distance = 0.59; % distance in miles LPR01 - LPR02 
%gh_distance = 12.6; % distance in miles LPR02 - LPR03

z = 9;
%%min_speed = 1; %mph
%%max_speed = 100; %mph
dth = 10; %sample time interval at station h (minutes)
%gtruth = 'true';
no_sync = 0; %minutes - synchronization correction

% ************************************************************************

prob_type = 1;

for f = 1:length(listfile)
display(['InputFile :', listfile(f).name]);
[M,e] = learning(f, z, dth, gh_distance, prob_type, ...
        min_speed, max_speed, no_sync, gtruth, listfile(f,:), directory_name, matrix_folder, z_value);
        %min_speed, max_speed, no_sync, gtruth, listfile(1:f,:), directory_name, matrix_folder);
    
end
% END^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^













