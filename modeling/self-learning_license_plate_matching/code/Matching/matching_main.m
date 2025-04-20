%% Mtching ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
%% Match two LPR datasets
%start_path = 'M:\';
%Select input and output folders -----------------------------------------
%%matrix_folder = uigetdir(start_path, 'Select Matrix folder');
%%input_folder = uigetdir(start_path, 'Select input folder');
%%output_folder = uigetdir(start_path, 'Select output folder');
% ------------------------------------------------------------------------

function [M, clocktime, nm, nf, p] = matching_main(matrix_folder, input_folder, output_folder,...
        min_speed, max_speed, gh_distance, gtruth)
% parameters settings ----------------------------------------------------
% Initial time-window
%%min_speed = 1; %mph
%%max_speed = 100; %mph
%%gh_distance = 0.224916739; % distance in miles between LPR01  and LPR02 

% Type of weight for the edit distance: use "weight" or "unitary"
type = 'weight';

% Groung truth
%gtruth = 'true';

% Initial time
dth = 10;

% Minutes - synchronization correction
no_sync = 0; 

% Type of probability function
type_prob = 1;

% Varying time window parameters
    z = 9;
    if type_prob == 1
        t_min = 5;
        t_max = 17.5;
    elseif type_prob == 2
        t_min = 5;
        t_max = 20;
    else
        t_min = 30;
        t_max = 40;
    end

% --------------------------------------------------------------
 
% Get file list of files 
listmatrix = dir(fullfile(matrix_folder ,'*Matrix*.*'));
listfile = dir(fullfile(input_folder ,'*lpr*.*'));

for n = 1:size(listmatrix,1) % to check Matrix
    display(['MatrixFile :', listmatrix(n).name]);
end

for n = 1:size(listfile,1) % to check Matrix
    display(['InputFile :', listfile(n).name]);
end

% Main Loop **************************************************************
match = cell(size(listmatrix,1),size(listfile,1)); 
clock = zeros(size(listmatrix,1),size(listfile,1)); 

for n = 1:size(listmatrix,1) % Matrix loop
     display(['matrix: ', listmatrix(n).name]);
    
    % Get matrix & convergence error
    cd(matrix_folder)
    data = importdata(listmatrix(n).name);
    W = data.AssociationMatrix;
    clear data
 
    % Edit weights for a given type of probality
    if type_prob ==1
        W = W./repmat(sum(W,2), 1, size(W,2));
    elseif type_prob == 2
        W = W./repmat(sum(W,1), size(W,1), 1);
    else
        W = W./sum(sum(W));
    end
        
       
        for f = 1:length(listfile) % File loop
                               
            infilename = listfile(f).name;
            [infilename_split, delimiter]=strsplit(infilename,'.');
            output_name = [infilename_split{1,1}, '_Output'];
            %output_name = [infilename(:), '_output'];      
            %output_name = [infilename(1:9), 'matrix', num2str(n)];      
        
            [M, clocktime, nm, nf, p] = matching(...
                    z, t_min, t_max, dth, gh_distance,...
                    min_speed, max_speed, no_sync, gtruth, infilename, input_folder, W, type, ...
                    output_name, output_folder);
              
    

        end
   
end
    
% *************************************************************************

% END OF MATCHING ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^