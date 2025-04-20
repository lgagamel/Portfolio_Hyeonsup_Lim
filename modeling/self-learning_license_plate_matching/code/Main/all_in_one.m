clear all;
close all;

matrix_folder = 'D:\MATLAB\20150307_LPR_Initial_AM\data\input\input1\matrix';
input_folder = 'D:\MATLAB\20150307_LPR_Initial_AM\data\input\input1';
output_folder = 'D:\MATLAB\20150307_LPR_Initial_AM\data\input\input1\output';

min_speed = 3; %mph
max_speed = 150; %mph
gh_distance = 3; % distance in miles between LPR01  and LPR02 
z_value= 1.645;
gtruth = 'true';

learning_main(input_folder, matrix_folder,...
        min_speed, max_speed, gh_distance, z_value, gtruth);

%matching_main(matrix_folder, input_folder, output_folder,...
%        min_speed, max_speed, gh_distance);



clear all;
close all;

matrix_folder = 'D:\MATLAB\20150307_LPR_Initial_AM\data\input\input2\matrix';
input_folder = 'D:\MATLAB\20150307_LPR_Initial_AM\data\input\input2';
output_folder = 'D:\MATLAB\20150307_LPR_Initial_AM\data\input\input2\output';

min_speed = 3; %mph
max_speed = 150; %mph
gh_distance = 3; % distance in miles between LPR01  and LPR02 
z_value= 1.645;
gtruth = 'true';

learning_main(input_folder, matrix_folder,...
        min_speed, max_speed, gh_distance, z_value, gtruth);

%matching_main(matrix_folder, input_folder, output_folder,...
%        min_speed, max_speed, gh_distance);

clear all;
close all;

matrix_folder = 'F:\004. MATLAB\001.Projects\20150308_LPR_InitialAM_I100\data\input\input3\matrix';
input_folder = 'F:\004. MATLAB\001.Projects\20150308_LPR_InitialAM_I100\data\input\input3';
output_folder = 'F:\004. MATLAB\001.Projects\20150308_LPR_InitialAM_I100\data\input\input3\output';

min_speed = 3; %mph
max_speed = 150; %mph
gh_distance = 3; % distance in miles between LPR01  and LPR02 
z_value= 1.645;
gtruth = 'true';

learning_main(input_folder, matrix_folder,...
        min_speed, max_speed, gh_distance, z_value, gtruth);

%matching_main(matrix_folder, input_folder, output_folder,...
%        min_speed, max_speed, gh_distance);
