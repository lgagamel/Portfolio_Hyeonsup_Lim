function [M, clocktime, nm, nf, p] = matching(...
    z, t_min, t_max, dth, gh_distance,...
    min_speed, max_speed, no_sync, gtruth, infilename, input_folder, W, type, ...
    output_name, output_folder)
% Function to match sets of LPR readings
te = clock;
cd(input_folder)

%Input ---------------------------------
M = zeros(37,37); %Estimate matrix
p = 0;  %Potential matches
nm = 0; %Number of matches
nf = 0; %Number of false matches
%---------------------------------------

% Time window constraint limits
jtu = 60*gh_distance/min_speed;  %Upper bound for jt
jtl = 60*gh_distance/max_speed;  %Lower bound for jt

%Read each worksheet of file f
[numg, textg, rawg] = xlsread(infilename, 1);
[numh, texth, rawh] = xlsread(infilename, 2);

%Time vectors for each station
u = cat(1,rawg{2:end,3})*24*60;
v = cat(1,rawh{2:end,3})*24*60;

%Variable allocation: Define matching, groung-truth and journey time vectors
match_set =         zeros(length(v),10);        % Contents: index_g, index_h, time_g, time_h, ED, ff, em, jt, mean_jt, stdv_jt
match_set(:,4) =    -1;                         % Initial flags for matching status: -1

match =         zeros(length(v),1);  %Contents: index in g
true_list =     zeros(length(v),1);  %Contents: index in g
jt =            [v, zeros(length(v),1)]; %Contents: time_h, Journey Time

match_set_1 ={};
match_set_other ={};
match_set_other_1 ={};


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
            
            D(i) = gened(xstr, ystr, W, type);
            
            % Determine if the match is an exact match
            if strmatch(xstr, ystr, 'exact')
                E(i) = 1;
            end
            
            % Check whether the match is true or false
            if strmatch(gtruth, 'true', 'exact')
                ytrue = strtest(rawh{j+1,5}); %Ground truth at h
                xtrue = strtest(rawg{i_ind(i)+1,5}); %Ground truth at g
                
                if strmatch(xtrue, ytrue, 'exact')==1
                    F(i) = 1;
                end
            end
        end
        
        %if size(ind_match)==0
        %    display('There is no match in this dataset');
        %else
        %
        %end
        
        %% Added by Hyeonsup - Start
        [DD ind_match_other]=sort(D,'ascend');
        if size(ind_match_other,2)>5
            ind_match_other = ind_match_other(1:5);
        else
            ind_match_other = ind_match_other(1:end);
        end
        
        ind_true_match = find(F==1);
        
        for ii=1:size(ind_true_match,2)
            temp_size = find(ind_match_other==ind_true_match(ii));
            if size(temp_size,2)==0;
                ind_match_other = [ind_match_other, ind_true_match(ii)];
            end
        end
        
        for kk = 1:size(ind_match_other,2)
            ind_match_other_kk = ind_match_other(kk);
            ed = D(ind_match_other_kk);
            ff = F(ind_match_other_kk);
            em = E(ind_match_other_kk);
            t_ij = v(j)-u(i_ind(ind_match_other_kk))-no_sync;
            
            %^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
            %Classification procedure ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            %if ~any(match == i_ind(ind_match_other_kk)) %index_match not found
            if v(j) - v(1) >= dth && length(find(jt(:,2)>0))>10 %Intial time shift or at least 10 observations
                
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
                
                %if ed <= t_min %Classify as genuine
                %match(j) = i_ind(kk);
                match_set_other =  [match_set_other; {i_ind(ind_match_other_kk), j, u(i_ind(ind_match_other_kk)), v(j),  ed, ff, em, t_ij, mean_jt, std_jt}];
                
                if strmatch(gtruth, 'true', 'exact')
                    match_set_other_1 = [match_set_other_1;{rawg{i_ind(ind_match_other_kk)+1,4}, rawh{j+1,4},rawg{i_ind(ind_match_other_kk)+1,5}, rawh{j+1,5}}];
                else
                    match_set_other_1 = [match_set_other_1;{rawg{i_ind(ind_match_other_kk)+1,4}, rawh{j+1,4}}];
                end
                if ff==1;
                    jt(j,:) = [v(j), t_ij];
                end
                
                
            elseif ff==1
                match_set_other =  [match_set_other; {i_ind(ind_match_other_kk), j, u(i_ind(ind_match_other_kk)), v(j),  ed, ff, em, t_ij, 999999, 999999}];
                
                if strmatch(gtruth, 'true', 'exact')
                    match_set_other_1 = [match_set_other_1;{rawg{i_ind(ind_match_other_kk)+1,4}, rawh{j+1,4},rawg{i_ind(ind_match_other_kk)+1,5}, rawh{j+1,5}}];
                else
                    match_set_other_1 = [match_set_other_1;{rawg{i_ind(ind_match_other_kk)+1,4}, rawh{j+1,4}}];
                end
                
                jt(j,:) = [v(j), t_ij];
            end
            %end
            
        end
        
        %% Added by Hyeonsup - End
        
        
        ind_match = find(D == min(D));
        ind_match = ind_match(1);
        
        ed = D(ind_match);
        ff = F(ind_match);
        em = E(ind_match);
        t_ij = v(j)-u(i_ind(ind_match))-no_sync;
        
        %^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        %Classification procedure ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if ~any(match == i_ind(ind_match)) %index_match not found
            if v(j) - v(1) >= dth && length(find(jt(:,2)>0))>10 %Intial time shift or at least 10 observations
                
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
                    match_set(j,:) =  [i_ind(ind_match), j, u(i_ind(ind_match)), v(j),  ed, ff, em, t_ij, mean_jt, std_jt];
                    
                    if strmatch(gtruth, 'true', 'exact')
                        match_set_1 = [match_set_1;{rawg{i_ind(ind_match)+1,4}, rawh{j+1,4},rawg{i_ind(ind_match)+1,5}, rawh{j+1,5}}];
                    else
                        match_set_1 = [match_set_1;{rawg{i_ind(ind_match)+1,4}, rawh{j+1,4}}];
                    end
                    
                    if ff==1
                        jt(j,:) = [v(j), t_ij];
                    end
                    %number of false matches
                    if ff == 0
                        nf = nf + 1;
                    end
                    
                elseif and(ed>t_min, ed<=t_max)
                    
                    %Time constraint - secondary **********************
                    if abs((t_ij - mean_jt)/std_jt) <=...
                            sqrt(z*(t_max - ed)/(t_max - t_min));
                        
                        match(j) = i_ind(ind_match);
                        match_set(j,:) =  [i_ind(ind_match), j, u(i_ind(ind_match)), v(j),  ed, ff, em, t_ij, mean_jt, std_jt];
                        if strmatch(gtruth, 'true', 'exact')
                            match_set_1 = [match_set_1;{rawg{i_ind(ind_match)+1,4}, rawh{j+1,4},rawg{i_ind(ind_match)+1,5}, rawh{j+1,5}}];
                        else
                            match_set_1 = [match_set_1;{rawg{i_ind(ind_match)+1,4}, rawh{j+1,4}}];
                        end
                        
                        if ff==1
                            jt(j,:) = [v(j), t_ij];
                        end
                        %number of false matches
                        if ff == 0
                            nf = nf + 1;
                        end
                        
                    end
                    %*************************************************
                end
                
                %elseif ed <= t_min
            elseif ff==1
                jt(j,:) = [v(j), t_ij];
            end
        end
        %^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
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
    
    display(['Matching_', infilename,' file completed...',num2str(j/length(v).*100), ' %'])
end
% End of main loop

%% Outcome <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
nm = nm +  length(find(match));  %Number of matches
p = p + length(find(true_list)); %Number of potential matches
match_set(match_set(:,1) == 0,:) = [];

%% <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

%Time performance of the algorithm
clocktime = etime(clock,te)/60;

%Output
%Matching----------------------------------------------------------

if isempty(match_set) == 0
    cd(output_folder);
    Contents = {'Index_g', 'Index_h', 'Time_g', 'Time_h', 'GED', 'True', 'Exact', 'Travel Time', 'Mean', 'STDV', 'Str_g', 'Str_h', 'True_Str_g', 'True_Str_h'};
    xlswrite(output_name, Contents , 'Match', 'A1');
    xlswrite(output_name, match_set , 'Match', 'A2');
    xlswrite(output_name, match_set_1 , 'Match', 'K2');
else
    display('There is no match in this dataset');
end

if isempty(match_set_other) == 0
    cd(output_folder);
    Contents = {'Index_g', 'Index_h', 'Time_g', 'Time_h', 'GED', 'True', 'Exact', 'Travel Time', 'Mean', 'STDV', 'Str_g', 'Str_h', 'True_Str_g', 'True_Str_h'};
    xlswrite(output_name, Contents , 'Match_other', 'A1');
    xlswrite(output_name, match_set_other , 'Match_other', 'A2');
    xlswrite(output_name, match_set_other_1 , 'Match_other', 'K2');
else
    display('There is no match in this dataset');
end
%------------------------------------------------------------------

clear match numg textg rawg  numh texth rawh
end



