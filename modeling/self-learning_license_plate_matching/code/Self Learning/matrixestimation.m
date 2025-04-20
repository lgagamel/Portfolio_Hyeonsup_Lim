function [M, nm, nf, p] = matrixestimation(m, z, t_min, t_max, dth, gh_distance,...
    min_speed, max_speed, no_sync, type, gtruth, listfile, input_folder, Initial, matrix_folder, prob_type, z_value)

%Sript to estimate the confusion matrix between the two stations

cd(input_folder)

clocktime = [];
%Input ---------------------------------
M = eye(37,37); %Estimate matrix
p = 0;  %Potential matches
nm = 0; %Number of matches
nf = 0; %Number of false matches
%---------------------------------------

n = size(listfile,1);



%Go through each file
for f = 1:size(listfile,1)
    te = clock;
    temp_length_match=0;
    
    % Time window constraint limits
    jtu = 60*gh_distance/min_speed;  %Upper bound for jt
    jtl = 60*gh_distance/max_speed;  %Lower bound for jt
    
    filename = listfile(f).name;
    
    %Read each worksheet of file f
    [numg, textg, rawg] = xlsread(filename, 1);
    [numh, texth, rawh] = xlsread(filename, 2);
    
    %Time vectors for each station
    u = cat(1,rawg{2:end,3})*24*60;
    v = cat(1,rawh{2:end,3})*24*60;
    
    %Variable allocation: Define matching, groung-truth and journey time vectors
    match_set =         zeros(length(v),8);         % Contents: index_g, index_h, ED, ff, em, jt, mean_jt, stdv_jt
    match_set(:,4) =    -1;                         % Initial flags for matching status: -1
    
    match =         zeros(length(v),1);  %Contents: index in g
    true_list =     zeros(length(v),1);  %Contents: index in g
    jt =            [v, zeros(length(v),1)]; %Contents: time_h, Journey Time
    
    Summary_1=[]; Summary_2=[]; Summary_3=[]; Summary_4=[]; Summary_5=[]; Summary_6=[]; Summary_7=[]; Summary_8=[]; Summary_9=[]
    
    %% Main loop
    for j = 1:length(v)
        
        ystr = strtest(rawh{j+1,4}); %Reading at h
        
        i_ind = find(and(u >= v(j)-jtu , u <= v(j)-jtl)); %Set of candidates at g
        
        if isempty(i_ind) == 0
            D = zeros(1,length(i_ind)); %Vector with values of ED
            F = zeros(1,length(i_ind)); %Vector to indentify false matches
            E = zeros(1,length(i_ind)); % Vector for exact matches
            
            %%Search for the best match for y^^^^^^^^^^^^^^^^^^^^^^
            for i = 1:length(i_ind)
                
                xstr = strtest(rawg{i_ind(i)+1,4}); %Reading at g
                
                D(i) = genedw(xstr, ystr, type);
                
                % Determine if the match is an exact match
                if strmatch(xstr, ystr, 'exact')
                    E(i) = 1;
                end
                
                if strmatch(gtruth, 'true', 'exact')
                    ytrue = strtest(rawh{j+1,5}); %Ground truth at h
                    xtrue = strtest(rawg{i_ind(i)+1,5}); %Ground truth at g
                    
                    if strmatch(xtrue, ytrue, 'exact')==1
                        F(i) = 1;
                    end
                end
            end
            
            ind_match = find(D == min(D));
            ind_match = ind_match(1);
            
            ed = D(ind_match);
            ff = F(ind_match);
            em = E(ind_match);
            t_ij = v(j)-u(i_ind(ind_match))-no_sync;
            
            %^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
            %Classification procedure ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            ind_matrix = [];
            if ~any(match == i_ind(ind_match)) %index_match not found
                if v(j) - v(1) >= dth && length(find(jt(:,2)>0))>10 %Intial time shift
                    
                    % Journey time
                    % Get the last matches that are greater than zero
                    ind_jt = find(jt(:,2)>0);
                    
                    x_jt =  jt(ind_jt(end-10+1:end),2);
                    med_jt =  median(x_jt);
                    std_jt = std(x_jt);
                    
                    %Eliminate outliers --------------------------------
                    ind_upper = find(x_jt > med_jt +3*std_jt);
                    ind_lower = find(x_jt < med_jt -3*std_jt);
                    
                    if isempty(ind_upper) == 0
                        x_jt(ind_upper) = [];
                    end
                    
                    if isempty(ind_lower) == 0
                        x_jt(ind_lower) = [];
                    end
                    
                    mean_jt =  mean(x_jt); % mean journey time after filtering
                    std_jt = std(x_jt);    % stdv of the journey time
                    %-------------------------------------------------
                    
                    if ed <= t_min %Classify as genuine
                        match(j) = i_ind(ind_match);
                        match_set(j,:) =  [i_ind(ind_match), j, ed, ff, em, t_ij, mean_jt, std_jt];
                        jt(j,:) = [v(j), t_ij];
                        
                        %number of false matches
                        if ff == 0
                            nf = nf + 1;
                        end
                        
                        %Ind_matrix -----------------------------------
                        xstr = strtest(rawg{i_ind(ind_match)+1,4}); %Reading at g
                        
                        [edist, W, w] = genedw(xstr, ystr, type);
                        ind_matrix = gedbtracking(W, w, xstr, ystr);
                        %----------------------------------------------
                        
                    elseif and(ed>t_min, ed<=t_max)
                        
                        %Time constraint - secondary **********************
                        if abs((t_ij - mean_jt)/std_jt) <=...
                                sqrt(z*(t_max - ed)/(t_max - t_min));
                            
                            match(j) = i_ind(ind_match);
                            match_set(j,:) =  [i_ind(ind_match), j, ed, ff, em, t_ij, mean_jt, std_jt];
                            jt(j,:) = [v(j), t_ij];
                            
                            %number of false matches
                            if ff == 0
                                nf = nf + 1;
                            end
                            
                            %Ind_matrix -----------------------------------
                            xstr = strtest(rawg{i_ind(ind_match)+1,4}); %Reading at g
                            
                            [edist, W, w] = genedw(xstr, ystr, type);
                            ind_matrix = gedbtracking(W, w, xstr, ystr);
                            %----------------------------------------------
                            
                        end
                        %*************************************************
                    end
                    
                elseif ed <= t_min
                    jt(j,:) = [v(j), t_ij];
                end
            end
            %^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
            %Updating matrix ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            if isempty(ind_matrix)==0
                for ind = 1:size(ind_matrix,1)
                    M(ind_matrix(ind,1),ind_matrix(ind,2))= ...
                        M(ind_matrix(ind,1),ind_matrix(ind,2))+1;
                end
            end
            %^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
            %Potential matches
            %-------------------------------------------------------------
            if ~any(true_list == i_ind(ind_match)) %Check if the match is already on true_list
                if v(j) - v(1) >= dth && length(find(jt(:,2)>0))>10
                    ind_true = find(F);
                    if ff == 1
                        true_list(j) = i_ind(ind_match);
                    elseif isempty(ind_true)==0
                        if ~any(true_list == i_ind(ind_true(1)))
                            true_list(j) = i_ind(ind_true(1));
                        end
                    end
                end
            end
            %-------------------------------------------------------------
            
        end
        
        %% Added code by Hyeonsup - Start
        
        if  or(and(mod(length(find(match)),25) == 0 && length(find(match))> 0  , length(find(match)) > temp_length_match), j==length(v))
            temp_length_match=length(find(match));
            
            Output_Matrix = Initial;
            
            if min((repmat(sum(M,2),1,37)))>0
                % Build 3 matrix Pi, Up, Down
                if prob_type == 1
                    B = M./(repmat(sum(M,2),1,size(M,2)));
                    Up = B+z_value.*((B.*(1-B)./(repmat(sum(M,2),1,size(M,2))))^0.5);
                    Down = B-z_value.*((B.*(1-B)./(repmat(sum(M,2),1,size(M,2))))^0.5);
                elseif prob_type == 2
                    B = M./(repmat(sum(M,1),size(M,1),1));
                    Up = B+z_value.*((B.*(1-B)./(repmat(sum(M,1),size(M,1),1)))^0.5);
                    Down = B-z_value.*((B.*(1-B)./(repmat(sum(M,1),size(M,1),1)))^0.5);
                else
                    B = M./sum(sum(M));
                    Up = B+z_value.*((B.*(1-B)./(sum(sum(M))))^0.5);
                    Down = B-z_value.*((B.*(1-B)./(sum(sum(M))))^0.5);
                end
                
                % Compare with initial Matrix & Update Association Matrix
                ind=find(not(and(Initial<Up,Initial>Down)));
                Output_Matrix(ind) = B(ind);
            end
            
            
            
            % Output Matrix
            [infilename_split, delimiter]=strsplit(filename,'.');
            output_name = [infilename_split{1,1}, '_Matrix_', num2str(m), '_', num2str(temp_length_match)];
            mkdir(matrix_folder,output_name);
            cd([matrix_folder, '\',output_name]);
            xlswrite(output_name, Output_Matrix , 'AssociationMatrix', 'B2');
            xlswrite(output_name, M , 'M', 'B2');
            xlswrite(output_name, Up , 'Up', 'B2');
            xlswrite(output_name, Down , 'Down', 'B2');
            matrix_folder_n=[matrix_folder, '\',output_name];
            
            
%             % Run Matching Algorithm (Method0-Using C.I.)
%             [M_1, clocktime_1, nm_1, nf_1, p_1] = matching_main(matrix_folder_n, input_folder, matrix_folder_n,...
%                 min_speed, max_speed, gh_distance, gtruth);
%             Summary_1=[Summary_1 ; 1, m, temp_length_match, clocktime_1, nm_1, nf_1, p_1];
%             cd([matrix_folder]);
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_1', 'A1');
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_1 , 'Summary_1', 'A2');
%             
%             % Run Matching Algorithm (Method2-Using Zero Matrix at Initial)
%             mkdir(matrix_folder,[output_name,'_2']);
%             cd([matrix_folder, '\',output_name,'_2']);
%             xlswrite([output_name,'_1'], M , 'AssociationMatrix', 'B2');
%             matrix_folder_n_2=[matrix_folder, '\',output_name,'_2'];
%             [M_2, clocktime_2, nm_2, nf_2, p_2] = matching_main(matrix_folder_n_2, input_folder, matrix_folder_n_2,...
%                 min_speed, max_speed, gh_distance, gtruth);
%             Summary_2=[Summary_2 ; 2, m, temp_length_match, clocktime_2, nm_2, nf_2, p_2];
%             cd([matrix_folder]);
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_2', 'A1');
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_2 , 'Summary_2', 'A2');
%             
%             % Run Matching Algorithm (Method3-Using N*eye Matrix at Initial)
%             N_initial=100;
%             mkdir(matrix_folder,[output_name,'_3']);
%             cd([matrix_folder, '\',output_name,'_3']);
%             xlswrite([output_name,'_3'], M+eye(37).*N_initial , 'AssociationMatrix', 'B2');
%             matrix_folder_n_3=[matrix_folder, '\',output_name,'_3'];
%             [M_3, clocktime_3, nm_3, nf_3, p_3] = matching_main(matrix_folder_n_3, input_folder, matrix_folder_n_3,...
%                 min_speed, max_speed, gh_distance, gtruth);
%             Summary_3=[Summary_3 ; 3, m, temp_length_match, clocktime_3, nm_3, nf_3, p_3];
%             cd([matrix_folder]);
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_3', 'A1');
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_3 , 'Summary_3', 'A2');
%             
%             % Run Matching Algorithm (Method4-Using N*eye Matrix at Initial)
%             N_initial=1000;
%             mkdir(matrix_folder,[output_name,'_4']);
%             cd([matrix_folder, '\',output_name,'_4']);
%             xlswrite([output_name,'_4'], M+eye(37).*N_initial , 'AssociationMatrix', 'B2');
%             matrix_folder_n_4=[matrix_folder, '\',output_name,'_4'];
%             [M_4, clocktime_4, nm_4, nf_4, p_4] = matching_main(matrix_folder_n_4, input_folder, matrix_folder_n_4,...
%                 min_speed, max_speed, gh_distance, gtruth);
%             Summary_4=[Summary_4 ; 4, m, temp_length_match, clocktime_4, nm_4, nf_4, p_4];
%             cd([matrix_folder]);
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_4', 'A1');
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_4 , 'Summary_4', 'A2');
%             
%             % Run Matching Algorithm (Method5-Using N*rand Matrix at Initial)
%             N_initial=1000;
%             mkdir(matrix_folder,[output_name,'_5']);
%             cd([matrix_folder, '\',output_name,'_5']);
%             xlswrite([output_name,'_5'], M+rand(37).*N_initial , 'AssociationMatrix', 'B2');
%             matrix_folder_n_5=[matrix_folder, '\',output_name,'_5'];
%             [M_5, clocktime_5, nm_5, nf_5, p_5] = matching_main(matrix_folder_n_5, input_folder, matrix_folder_n_5,...
%                 min_speed, max_speed, gh_distance, gtruth);
%             Summary_5=[Summary_5 ; 5, m, temp_length_match, clocktime_5, nm_5, nf_5, p_5];
%             cd([matrix_folder]);
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_5', 'A1');
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_5 , 'Summary_5', 'A2');
%             
%             % Run Matching Algorithm (Method6-Using Previous M Matrix at Initial)
%             
%             cd(input_folder)
%             list_Previous_M = dir(fullfile(input_folder ,'*Previous_M1*.*'));
%             data = importdata(list_Previous_M(1).name);
%             Previous_M = data.AssociationMatrix;
%             
%             mkdir(matrix_folder,[output_name,'_6']);
%             cd([matrix_folder, '\',output_name,'_6']);
%             xlswrite([output_name,'_6'], M+Previous_M , 'AssociationMatrix', 'B2');
%             matrix_folder_n_6=[matrix_folder, '\',output_name,'_6'];
%             [M_6, clocktime_6, nm_6, nf_6, p_6] = matching_main(matrix_folder_n_6, input_folder, matrix_folder_n_6,...
%                 min_speed, max_speed, gh_distance, gtruth);
%             Summary_6=[Summary_6 ; 6, m, temp_length_match, clocktime_6, nm_6, nf_6, p_6];
%             cd([matrix_folder]);
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_6', 'A1');
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_6 , 'Summary_6', 'A2');
%             
            % Run Matching Algorithm (Method7-Using N*eye+1 Matrix at Initial)
            N_initial=100;
            mkdir(matrix_folder,[output_name,'_7']);
            cd([matrix_folder, '\',output_name,'_7']);
            xlswrite([output_name,'_7'], M+eye(37).*N_initial+1 , 'AssociationMatrix', 'B2');
            matrix_folder_n_7=[matrix_folder, '\',output_name,'_7'];
            [M_7, clocktime_7, nm_7, nf_7, p_7] = matching_main(matrix_folder_n_7, input_folder, matrix_folder_n_7,...
                min_speed, max_speed, gh_distance, gtruth);
            Summary_7=[Summary_7 ; 7, m, temp_length_match, clocktime_7, nm_7, nf_7, p_7];
            cd([matrix_folder]);
            xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_7', 'A1');
            xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_7 , 'Summary_7', 'A2');
            
            
%             % Run Matching Algorithm (Method8-Using Previous M Matrix+1 at Initial)
%             cd(input_folder)
%             list_Previous_M = dir(fullfile(input_folder ,'*Previous_M1*.*'));
%             data = importdata(list_Previous_M(1).name);
%             Previous_M = data.AssociationMatrix;
%             
%             mkdir(matrix_folder,[output_name,'_8']);
%             cd([matrix_folder, '\',output_name,'_8']);
%             xlswrite([output_name,'_8'], M+Previous_M+1 , 'AssociationMatrix', 'B2');
%             matrix_folder_n_8=[matrix_folder, '\',output_name,'_8'];
%             [M_8, clocktime_8, nm_8, nf_8, p_8] = matching_main(matrix_folder_n_8, input_folder, matrix_folder_n_8,...
%                 min_speed, max_speed, gh_distance, gtruth);
%             Summary_8=[Summary_8 ; 8, m, temp_length_match, clocktime_8, nm_8, nf_8, p_8];
%             cd([matrix_folder]);
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_8', 'A1');
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_8 , 'Summary_8', 'A2');
%             
%             
%             % Run Matching Algorithm (Method9-Using Previous M2 Matrix+1 at Initial)
%             cd(input_folder)
%             list_Previous_M = dir(fullfile(input_folder ,'*Previous_M2*.*'));
%             data = importdata(list_Previous_M(1).name);
%             Previous_M = data.AssociationMatrix;
%             
%             mkdir(matrix_folder,[output_name,'_9']);
%             cd([matrix_folder, '\',output_name,'_9']);
%             xlswrite([output_name,'_9'], M+Previous_M+1 , 'AssociationMatrix', 'B2');
%             matrix_folder_n_9=[matrix_folder, '\',output_name,'_9'];
%             [M_9, clocktime_9, nm_9, nf_9, p_9] = matching_main(matrix_folder_n_9, input_folder, matrix_folder_n_9,...
%                 min_speed, max_speed, gh_distance, gtruth);
%             Summary_9=[Summary_9 ; 9, m, temp_length_match, clocktime_9, nm_9, nf_9, p_9];
%             cd([matrix_folder]);
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], {'Index for Association Matrix', 'iteration', 'No.of Matches of Association Matrix', 'clocktime', 'Number of matches', 'Number of false matches ', 'Number of potential matches'} , 'Summary_9', 'A1');
%             xlswrite([infilename_split{1,1},'_Output_Summary_', num2str(m)], Summary_9 , 'Summary_9', 'A2');
%             
            
            [~,computer] = system('hostname');
            [~,user] = system('whoami');
            [~,alltask] = system(['tasklist /S ', computer, ' /U', user]);
            excelPID=regexp(alltask, 'EXCEL.EXE\s*(\d+)\s','tokens');
            for k=1:length(excelPID)
                killPID=cell2mat(excelPID{k});
                system(['taskkill /f /pid ', killPID]);
            end
            
        end
        %infilename = listfile.name;
        display(['Self-Learning_', filename,' file completed...',num2str(j/length(v).*100), ' %'])
        
        
        %% Added code by Hyeonsup - End
        
    end
    % End of main loop
    
    %% Outcome <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    nm = nm +  length(find(match));  %Number of matches
    p = p + length(find(true_list)); %Number of potential matches
    match_set = [match_set, true_list];
    match_set(match_set(:,1) == 0,:) = [];
    %% <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    %Time performance of the algorithm
    clocktime = [clocktime; etime(clock,te)/60];
    display(clocktime(f));
    
    %Output
    %     %Matching----------------------------------------------------------
    %     xlswrite(['GED_Match', num2str(f)], match_set , ['Output_Matrix',  num2str(n), num2str(m)], 'A2');
    %     %------------------------------------------------------------------
    
    
    clear match numg textg rawg  numh texth rawh
end




